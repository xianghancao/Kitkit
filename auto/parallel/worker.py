# coding=utf-8
# 20180426
import numpy as np
import pandas as pd
from munch import Munch
import json, os
from prob_engine import ProbEngine
from data_structure import DataStructure
from backtest import BackTest
from operators import *
from tqdm import tqdm
from datetime import datetime
from pymongo import MongoClient
import multiprocessing
from multiprocessing import Process, Queue, Pool
from multiprocessing.managers import BaseManager
import time

def Backtester(exprDict):
    backtest_conf = {'backtest_start':'2019-07-01',
                    'backtest_end': '2019-11-01',
                    'data_path': '/home/fbillion/15min/',
                    'maxlookback': 200,
                    'quintiles': 5,
                    'cost': 0.,
                    'cycle': '15MIN'}

    exprDict.update(backtest_conf)


     

    try:

        #step 1 data------------------------------------------------------------------------------------
        from data.pricevolume import PriceVolume
        pv = PriceVolume(path=backtest_conf['data_path'])
        pv.build()

        #step2 resample------------------------------------------------------------------------------------
        from data.resample import Resample
        rs = Resample(IS_start=backtest_conf['backtest_start'], IS_end=backtest_conf['backtest_end'])
        IS_Data = rs.build(pv)


        #step3 alpha------------------------------------------------------------------------------------
        ClosePrice = IS_data.ClosePrice
        OpenPrice = IS_data.OpenPrice
        HighestPrice = IS_data.HighestPrice
        LowestPrice = IS_data.LowestPrice
        Volume = IS_data.Volume
        Amount = IS_data.Amount
        VWAP = IS_data.VWAP
        Return = IS_data.Return
        Turnover = IS_data.Trunover

        alpha = eval(exprDict['expr'])
        exprDict['cal_error'] = None

        #step4 deal------------------------------------------------------------------------------------
        from traders.open_deal import OpenDeal
        dealObj=OpenDeal(IS_Data, alpha=alpha, maxlookback=backtest_conf['maxlookback'])
        dealObj.build()


        #step5 performance------------------------------------------------------------------------------------
        from evaluators.alpha_perform import AlphaPerform
        ap = AlphaPerform(dealObj, cost=backtest_conf['cost'], cycle=backtest_conf['cycle'], quintiles_num=backtest_conf['quintiles'], figure=False)
        ap.build()

        print '[layer%s] %s calculating ...' %(exprDict['layer'], exprDict['expr'])
        exprDict.update(ap.indicators)
        exprDict['backtest'] = 'Done'
        return exprDict

    except Exception as e:
        exprDict['cal_error'] = str(e)
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
        self.config.queue_authkey = 'abc'
        self.config.launch_time = time.strftime('%Y-%m-%d %H:%M:%S')

    # ------------------------连接queue------------------------
    def queue_connect(self):
        QueueManager.register('get_task_queue')
        m = QueueManager(address=('127.0.0.1', 5000), authkey='abc')
        m.connect()
        return m.get_task_queue()

    # -----------------------从queue获取任务------------------------
    def get_one_task(self):
        value = self.queue.get(True)
        return value


    # -----------------------连接mongodb------------------------
    def mongodb_connect(self):
        try:
            client = MongoClient(self.config.db_host, self.config.db_port)
            db = client[self.config.db_name]
        except Exception, e:
            print e, 'Connect to mongodb error'
        return db



    # -----------------------写入mongodb------------------------
    def update_mongodb(self, expr_dict):
        for iterm in expr_dict.keys():
            self.mongodb['layer%s' %expr_dict['layer']].update_one({'_id': expr_dict['_id']}, {"$set": {iterm: expr_dict[iterm]}})



    # -----------------------执行入口------------------------
    def run(self):
        # 连接队列
        self.queue  = self.queue_connect()
        # 连接数据库
        self.db = self.mongodb_connect()
        # 获取任务
        expr_dict = self.get_one_task()
        # 回测
        Backtester(expr_dict)
        #返回更新
        self.update_mongodb(expr_dict)




if __name__ == '__main__':
    w = Worker(db_host='127.0.0.1', db_port=27017, db_name='AutoResearch')
    w.run()

















