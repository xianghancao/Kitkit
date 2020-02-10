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
sys.path.append('/home/fbillion/Kitkit/')
from operators import *


def Backtester(exprDict):
    print('[Worker] Backtesting ...')
    backtest_conf = {'backtest_start':'2019-07-01',
                    'backtest_end': '2019-11-01',
                    'data_path': '/home/fbillion/15min/',
                    'maxlookback': 200,
                    'quintiles': 5,
                    'cost': 0.,
                    'cycle': '15MIN'}

    exprDict.update(backtest_conf)


     

#try
    #step 1 data------------------------------------------------------------------------------------
    from data.pricevolume import PriceVolume
    pv = PriceVolume(path=backtest_conf['data_path'])
    pv.build()

    #step2 resample------------------------------------------------------------------------------------
    from data.resample import Resample
    rs = Resample(IS_start=backtest_conf['backtest_start'], IS_end=backtest_conf['backtest_end'])
    IS_Data = rs.build(pv)


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
    exprDict['cal_error'] = None

    #step4 deal------------------------------------------------------------------------------------
    from traders.open_deal import OpenDeal
    dealObj=OpenDeal(IS_Data, alpha=alpha, maxlookback=backtest_conf['maxlookback'])
    dealObj.build()


    #step5 performance------------------------------------------------------------------------------------
    from evaluators.alpha_perform import AlphaPerform
    ap = AlphaPerform(dealObj, 
                      cost=backtest_conf['cost'], 
                      cycle=backtest_conf['cycle'], 
                      quintiles_num=backtest_conf['quintiles'], 
                      figure=False,
                      stat_info=True)
    ap.build()

    print('[layer%s] %s calculating ...' %(exprDict['layer'], exprDict['expr']))
    exprDict.update(ap.indicators)
    exprDict['backtest'] = 'Done'
    return exprDict


#     except Exception as e:
#         exprDict['cal_error'] = str(e)
#         print(e)
#         return exprDict
    



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
            client = MongoClient(self.config.db_host, self.config.db_port)
            self.mongodb = client[self.config.db_name]
            print('[Worker] mongodb connected')
        except Exception as e:
            print('[Worker] error:' + e)
            

    # -----------------------写入mongodb------------------------
    def update_mongodb(self, expr_dict):
        print(expr_dict)
        print('[Worker] mongodb update layer:%s _id:%s expr:%s create_date:%s' %(expr_dict['layer'], 
                                                                                 expr_dict['_id'], 
                                                                                 expr_dict['expr'],
                                                                                 expr_dict['create_date']))
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
    while 1:
        w = Worker(db_host='127.0.0.1', db_port=27017, db_name='AutoResearch')
        w.run()

















