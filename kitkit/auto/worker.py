# coding=utf-8
# 20180426
import numpy as np
from munch import Munch
from datetime import datetime
from pymongo import MongoClient
import multiprocessing
from multiprocessing import Process, Queue, Pool
from multiprocessing.managers import BaseManager
import time
import os, sys
sys.path.append('/share/Kitkit/kitkit/')
from operators import *

def load_version():
    version = {}
    with open('/share/Kitkit/kitkit/version.md') as f:
        for line in f.readlines():
            if len(line) > 2:
                version[line.split('=')[0].strip()] = line.split('=')[1].strip()
    return version

version = load_version()

def connect_mongodb(db_nname):
    settings = Munch()
    settings.MONGO_USER = 'admin'
    settings.MONGO_PSW = 'admin123'
    settings.MONGO_HOST = '127.0.0.1'
    settings.MONGO_PORT = '27017'
    client = MongoClient('mongodb://{0}:{1}@{2}:{3}'.format(settings.MONGO_USER,settings.MONGO_PSW,settings.MONGO_HOST,settings.MONGO_PORT))
    db = client[db_nname]
    return db


def Backtester(exprDict):
    print('[Worker] Backtesting ...')
    backtest_conf = {'resample_start':'2019-08-01',
                    'resample_end': '2019-12-01',
                    'data_path': '/share/Kitkit/data/930678_15min_6t/',
                    'maxlookback': 200,
                    'cost': 0.0015,
                    'cycle': '15MIN'}

    exprDict.update(backtest_conf)


     

    try:
        # from data.universe import Universe
        # u = Universe('/share/Kitkit/data/H30184cons.xls')
        # ticker = u.build()
        #step 1 data------------------------------------------------------------------------------------
        from data.pricevolume import PriceVolume
        pv = PriceVolume(path=backtest_conf['data_path'])
        pv.build()

        #step2 resample------------------------------------------------------------------------------------
        from data.resample import Resample
        rs = Resample(IS_start=backtest_conf['resample_start'], IS_end=backtest_conf['resample_end'])
        IS_Data, OOS_Data = rs.build(pv)

        from data.clean import Clean
        rs = Clean()
        IS_Data = rs.build(IS_Data)

        #step3 alpha------------------------------------------------------------------------------------
        ClosePrice = IS_Data.ClosePrice
        OpenPrice = IS_Data.OpenPrice
        HighestPrice = IS_Data.HighestPrice
        LowestPrice = IS_Data.LowestPrice
        Volume = IS_Data.Volume
        VWAP = IS_Data.VWAP
        Return = IS_Data.Return
        VolChg = IS_Data.VolChg

        alpha = eval(exprDict['expr'])
        alpha = pd.DataFrame(alpha).fillna(0).values

        #alpha保留正值
        alpha = alpha * (alpha>0)
        exprDict['cal_error'] = None

        #step4 deal------------------------------------------------------------------------------------
        from traders.open_deal import OpenDeal
        dealObj=OpenDeal(IS_Data, alpha=alpha, maxlookback=backtest_conf['maxlookback'])
        dealObj.build()


        #step5 performance------------------------------------------------------------------------------------
        from evaluators.benchmark_alpha_perform import BechmarkAlphaPerform
        ap = BechmarkAlphaPerform(dealObj, 
                          cost=backtest_conf['cost'], 
                          cycle=backtest_conf['cycle'], 
                          figure=False,
                          stat_info=False)
        ap.build()
        
        exprDict.update(ap.indicators)
        exprDict['backtest'] = 'Done'
    except Exception as e:
        print('[Worker][Backtester] raise Exception:%s' %e)
        exprDict['cal_error'] = str(e)
        exprDict['backtest'] = 'Error'
    return exprDict


class QueueManager(BaseManager):
    pass



# =================================================== worker =====================================================================
class Worker():
    # worker的手臂
    # 连接task queue
    # 连接mongodb
    def __init__(self, db_host, db_port, db_name):
        self.config = Munch()
        self.config.db_host = db_host
        self.config.db_port = db_port
        self.config.db_name = db_name

        self.config.queue_host = db_host
        self.config.queue_port = 5000
        self.config.queue_authkey = b'abc'
        self.config.launch_time = time.strftime('%Y-%m-%d %H:%M:%S')

    # ------------------------连接queue------------------------
    def queue_connect(self):
        QueueManager.register('get_task_queue')
        m = QueueManager(address=(self.config.queue_host, self.config.queue_port), authkey=self.config.queue_authkey)
        m.connect()
        print('[Worker] queue connected!')
        self.queue = m.get_task_queue()


    # -----------------------从queue获取任务------------------------
    def get_one_task(self):
        value = self.queue.get(True)
        print('[Worker] task acquired %s' %value)
        return value


    # -----------------------连接mongodb------------------------
    def mongodb_connect(self):
        try:
            self.mongodb = connect_mongodb(self.config.db_name)
            print('[Worker] mongodb connected')
        except Exception as e:
            print('[Worker] error:' + e)
            

    # -----------------------写入mongodb------------------------
    def update_mongodb(self, expr_dict):
        print('[Worker] mongodb update layer:%s _id:%s expr:%s create_date:%s' %(expr_dict['layer'], 
                                                                                 expr_dict['_id'], 
                                                                                 expr_dict['expr'],
                                                                                 expr_dict['create_date']))
        expr_dict['update_date'] = str(datetime.now())[:19]
        for iterm in expr_dict.keys():
            self.mongodb['layer%s' %expr_dict['layer']].update_one({'_id': expr_dict['_id']}, {"$set": {iterm: expr_dict[iterm]}})



    # -----------------------执行入口------------------------
    def run(self):
        # 连接队列
        self.queue_connect()
        # 连接数据库
        self.mongodb_connect()
        # 获取任务
        expr_dict = self.get_one_task()
        # 回测
        Backtester(expr_dict)
        #返回更新
        self.update_mongodb(expr_dict)




if __name__ == '__main__':
    w = Worker(db_host='127.0.0.1', db_port=27017, db_name='AutoResearch')
    print('-'*80)
    # 连接队列
    w.queue_connect()
    # 连接数据库
    w.mongodb_connect()
    
    while True:
        print('-'*30 + time.strftime('%H:%M') + ' V' + version['__version__'].replace("\"", "") + '-'*30)
        # 获取任务
        expr_dict = w.get_one_task()
        # 回测
        Backtester(expr_dict)
        #返回更新
        w.update_mongodb(expr_dict)


















