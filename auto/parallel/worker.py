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

# ================================================ Porter =======================================================
class QueueManager(BaseManager):
    pass


class Porter():
    # worker的手臂
    # 连接task queue
    # 连接mongodb
    def __init__(self, db_host, db_port, db_name, db_collection):
        self.config = Munch()
        self.config.db_host = db_host
        self.config.db_port = db_port
        self.config.db_name = db_name
        self.config.db_collection = db_collection

        self.config.queue_host = db_host
        self.config.queue_port = 5000
        self.config.queue_authkey = 'abc'
        self.config.launch_time = time.strftime('%Y-%m-%d %H:%M:%S')

        self.queue  = self.queue_connect()
        self.db = self.mongodb_connect()

    # ------------------------连接queue------------------------
    def queue_connect(self):
        QueueManager.register('get_task_queue')
        m = QueueManager(address=('127.0.0.1', 5000), authkey='abc')
        m.connect()
        return m.get_task_queue()


    # -----------------------连接mongodb------------------------
    def mongodb_connect(self):
        try:
            client = MongoClient(self.config.db_host, self.config.db_port)
            db = client[self.config.db_name]
        except Exception, e:
            print e, 'Connect to mongodb error'
        return db

    # -----------------------从queue获取任务------------------------
    def get_one_task(self):
        value = self.queue.get(True)
        return value


    # -----------------------写入mongodb------------------------
    def update_mongodb(self, data_structure_object):
        data_structure_object.update_mongodb(self.db)



# =================================================== worker =====================================================================
"""
功能
- 启动Porter
- 连接queue
- 连接mongodb
- 从queue获取task 
- 计算表达式
- 初步回测信号，产生sharpe值
- 结果写入mongodb
- 循环

"""

def delay(x, period=1):
    """
    [Definition] 序列x中前period天的价格
    [Category] 技术指标
    delay() value of x d days ago
    """
    res = np.zeros(x.shape) * np.nan
    res[period:] = x[:-period]
    return res


class Worker():
    def __init__(self, db_host, db_port, db_name, db_collection):
        self.porter = Porter(db_host, db_port, db_name, db_collection)
        
    def get_one_alpha(self):
        expr_dict = self.porter.get_one_task()
        self.expr_ds = DataStructure(expr_dict)



    def run(self):
        self.prepare_backtest_data()
        while True:
            self.get_one_alpha()
            self.cal_one_alpha()
            self.save_one_alpha()


    def prepare_backtest_data(self):
        # 切割样本IS，OOS
        eod_path = 'eod'
        dates = np.load(os.path.join('/mnt/ssd/', eod_path, '1day/dates.npy'))
        start_idx = 0 #np.where(dates >= '2013-02-04 09:00:00')[0][0]
        end_idx = np.where(dates >= '2016-03-01 09:00:00')[0][0]
        print 'backtest start:', dates[start_idx], 'end:', dates[end_idx]
        self.backtest_start = dates[start_idx]
        self.backtest_end = dates[end_idx]


        # 加载数据
        self.eod = Munch()
        self.eod.dates = dates[start_idx:end_idx]
        self.eod.ticker_names = np.load(os.path.join('/mnt/ssd/', eod_path, '1day/ticker_names.npy'))
        for i in ['OpenPrice', 'ClosePrice', 'HighestPrice', 'LowestPrice', 'Volume', 'VWAP', 'Position', 'TurnOver']:
            self.eod[i] = np.load(os.path.join('/mnt/ssd/', eod_path, '1day', i + '.npy')).T[start_idx:end_idx]
        self.eod.Return = self.eod.ClosePrice*1./delay(self.eod.ClosePrice, 1) - 1
        self.eod.Return = self.eod.Return[start_idx:end_idx]

        # 求收益率
        OpenPrice = pd.DataFrame(self.eod.OpenPrice)
        self.resample_returns = pd.DataFrame((OpenPrice.shift(-1)*1./OpenPrice-1).values[1:],
                                             index=self.eod.dates[1:],
                                             columns=self.eod.ticker_names)



    def cal_one_alpha(self):
        start_time = time.time()
        # 替换表达式
        expr_tmp = self.expr_ds.values.expr
        for i in ['OpenPrice', 'ClosePrice', 'HighestPrice', 'LowestPrice', 'Volume', 'VWAP', 'Position', 'TurnOver', 'Return']:
            expr_tmp = expr_tmp.replace(i, 'self.eod.' + i)

        # 计算信号
        try:
            alphas = eval(expr_tmp)
        except Exception, e:
            self.expr_ds.values.cal_error = 'cal_one_alpha compute error:' + str(e)
            print self.expr_ds.values.cal_error
            return 

        # 回测信号
        try:
            resample_wgts = pd.DataFrame(alphas[:-1] * 1., index=self.eod.dates[1:], columns=self.eod.ticker_names)
            self.bt = BackTest(resample_wgts.iloc[200:], returns=self.resample_returns.iloc[200:], cycle='day',
                        IS_OOS_ratio=None, stat_info=False, plot=False,
                        quintiles=3, turnover=1, cost=0., ticker_names=None,
                        output_dir=None, test_mode=False, signal_name=None)
       
            self.bt.stat_quintiles()
            self.bt.stat_quintiles_pnl()
            self.bt.stat_alpha_pnl()
            self.bt.stat_alpha_sharpe()
            self.bt.stat_trade_nums()
            print '[layer%s] %s sharpe:%s' %(self.expr_ds.values.layer, self.expr_ds.values.expr, self.bt.alpha_sharpe)
            self.expr_ds.values.IS_alpha_sharpe = round(self.bt.alpha_sharpe, 5)
            self.expr_ds.values.IS_alpha_pnl = round(self.bt.alpha_pnl[-1], 5)
            self.expr_ds.values.IS_backtest_start = self.backtest_start
            self.expr_ds.values.IS_backtest_end = self.backtest_end
            self.expr_ds.values.IS_backtest_sample_num = int(self.bt.trade_nums)

        except Exception, e:
            self.expr_ds.values.IS_error = '[layer%s] %s error:%s' %(self.expr_ds.values.layer, self.expr_ds.values.expr, str(e))
            print self.expr_ds.values.IS_error


        self.expr_ds.values.cost_time = round(time.time() - start_time, 5)
        return     
        


    def save_one_alpha(self):
        # 保存信号
        self.expr_ds.values.IS_backtest = 'Done'
        self.expr_ds.values.IS_cal_time = str(datetime.now())[:19]
        self.porter.update_mongodb(self.expr_ds)
        return








if __name__ == '__main__':
    w = Worker(db_host='127.0.0.1', db_port=27017, db_name='Machine', db_collection='layer2')
    w.run()

















