# coding=utf-8
# 20180426
import numpy as np
import pandas as pd
from munch import Munch
import json, os, sys

from data_structure import DataStructure
sys.path.append('/home/dev/')
from FalconAlpha.simlib.process.backtest import BackTest
from FalconAlpha.operators import *
from tqdm import tqdm
from datetime import datetime
import time




class AlphaCal():
    """
    计算指定alpha_ds的回测结果
    """
    def __init__(self, sampling):
        self.sampling = sampling
        self.prepare_backtest_data()


    def prepare_backtest_data(self):
        # 切割样本IS，OOS
        self.eod_path = 'Policy_eod2_f'
        dates = np.load(os.path.join('/mnt/ssd/', self.eod_path, '1day/dates.npy'))
        if self.sampling == 'IS':
            start_idx = np.where(dates > '2012-01-04 09:00:00')[0][0]
            end_idx = np.where(dates > '2016-03-01 09:00:00')[0][0]
        elif self.sampling == 'OOS1':
            start_idx = np.where(dates > '2014-01-04 09:00:00')[0][0]
            end_idx = np.where(dates > '2017-06-01 09:00:00')[0][0]
        elif self.sampling == 'OOS2':
            start_idx = np.where(dates > '2015-01-04 09:00:00')[0][0]
            end_idx = np.where(dates > '2018-03-01 09:00:00')[0][0]
        elif self.sampling == 'IS+OOS1':
            start_idx = np.where(dates > '2012-01-04 09:00:00')[0][0]
            end_idx = np.where(dates > '2017-06-01 09:00:00')[0][0]
        elif self.sampling == 'ALL':
            start_idx = np.where(dates > '2012-01-04 09:00:00')[0][0]
            end_idx = len(dates)-1
        else:
            raise Exception()

        # 加载数据
        self.eod = Munch()
        self.eod.dates = dates[start_idx:end_idx]
        self.eod.ticker_names = np.load(os.path.join('/mnt/ssd/', self.eod_path, '1day/ticker_names.npy'))
        for i in ['OpenPrice', 'ClosePrice', 'HighestPrice', 'LowestPrice', 'Volume', 'VWAP', 'Position', 'TurnOver']:
            self.eod[i] = np.load(os.path.join('/mnt/ssd/', self.eod_path, '1day', i + '.npy')).T[start_idx:end_idx]
        self.eod.Return = self.eod.ClosePrice*1./delay(self.eod.ClosePrice, 1) - 1
        self.eod.Return = self.eod.Return

        # 求收益率
        OpenPrice = pd.DataFrame(self.eod.OpenPrice)
        self.resample_returns = pd.DataFrame((OpenPrice.shift(-1)*1./OpenPrice-1).values[1:],
                                             index=self.eod.dates[1:],
                                             columns=self.eod.ticker_names)

        # 回测参数
        if self.sampling == 'IS':
            self.backtest_start_idx = np.where(self.eod.dates>'2013-01-04 09:00:00')[0][0]
            self.backtest_end_idx = np.where(self.eod.dates>='2016-03-01 09:00:00')[0][0]
        elif self.sampling == 'OOS1':
            self.backtest_start_idx = np.where(self.eod.dates>='2016-03-01 09:00:00')[0][0]
            self.backtest_end_idx = np.where(self.eod.dates>='2017-06-01 09:00:00')[0][0]
        elif self.sampling == 'OOS2':
            self.backtest_start_idx = np.where(self.eod.dates>='2017-06-01 09:00:00')[0][0]
            self.backtest_end_idx = np.where(self.eod.dates>='2018-03-01 09:00:00')[0][0]
        elif self.sampling == 'IS+OOS1':
            self.backtest_start_idx = np.where(self.eod.dates>'2013-01-04 09:00:00')[0][0]
            self.backtest_end_idx = np.where(self.eod.dates>='2016-06-01 09:00:00')[0][0]
        elif self.sampling == 'ALL':
            self.backtest_start_idx = np.where(self.eod.dates>'2013-01-04 09:00:00')[0][0]
            self.backtest_end_idx = len(self.eod.dates)-1
        else:
            raise Exception()
        self.backtest_start = self.eod.dates[self.backtest_start_idx]
        self.backtest_end = self.eod.dates[self.backtest_end_idx]
        print 'backtest start:', self.backtest_start
        print 'backtest end:', self.backtest_end
        time.sleep(1)
        return True



    def cal_one_alpha(self, alpha_ds, noise=False, output_dir=None):
        start_time = time.time()
        # 替换表达式
        expr_tmp = alpha_ds.values.expr
        # copy 
        eod_copy = Munch()
        for i in ['OpenPrice', 'ClosePrice', 'HighestPrice', 'LowestPrice', 'Volume', 'VWAP', 'Position', 'TurnOver', 'Return']:
            expr_tmp = expr_tmp.replace(i, 'eod_copy.' + i)
            setattr(eod_copy, i, getattr(self.eod, i).copy())


        # noise
        if noise:
            from random_history_data import RandomHistoryData
            self.rhd = RandomHistoryData(eod_copy, prob=0.1, data_range=0.1)
            eod_copy = self.rhd.gen_STD_noise()


        # 计算信号
        try:
            alphas_val = eval(expr_tmp)
        except Exception, e:
            alpha_ds.values.cal_error = str(e)
            print '[layer%s] %s cal_error:%s' %(alpha_ds.values.layer, alpha_ds.values.expr, str(e))
            return 

        # 回测信号
        try:
            resample_wgts = pd.DataFrame(alphas_val[:-1] * 1., index=self.eod.dates[1:], columns=self.eod.ticker_names)
            #resample_wgts.to_csv(output_dir+'/resample_wgts.csv')
            #self.resample_returns.to_csv(output_dir+'/resample_returns.csv')
            resample_returns = self.resample_returns.copy()
            self.bt = BackTest(resample_wgts.iloc[self.backtest_start_idx:], returns=resample_returns.iloc[self.backtest_start_idx:],
                         cycle='day',
                        IS_OOS_ratio=None, stat_info=False, plot=False,
                        quintiles=3, turnover=1, cost=0., ticker_names=None,
                        output_dir=output_dir, dump=False, signal_name=str(alpha_ds.values._id))
        
            self.bt.stat_quintiles()
            self.bt.stat_quintiles_pnl()
            self.bt.stat_alpha_pnl()
            self.bt.stat_alpha_sharpe()
            self.bt.stat_trade_nums()
            #pd.DataFrame(self.bt.alpha_cpnl, index=self.bt.resample_dates).to_csv(output_dir+'/alpha_cpnl.csv')

            alpha_ds.values.eod_version = self.eod_path
            alpha_ds.values.dtype = str(alphas_val.dtype)
            setattr(alpha_ds.values, '%s_alpha_sharpe' %self.sampling, round(self.bt.alpha_sharpe, 5))
            setattr(alpha_ds.values, '%s_alpha_pnl' %self.sampling,  round(self.bt.alpha_cpnl[-1], 5))
            setattr(alpha_ds.values, '%s_backtest_start' %self.sampling,  self.backtest_start)
            setattr(alpha_ds.values, '%s_backtest_end' %self.sampling,  self.backtest_end)
            setattr(alpha_ds.values, '%s_backtest_sample_num' %self.sampling,  int(self.bt.trade_nums))


        except Exception, e:
            setattr(alpha_ds.values, '%s_error' %self.sampling, str(e))
            print '[layer%s] %s %s_error:%s' %(alpha_ds.values.layer, alpha_ds.values.expr, self.sampling, str(e))



        alpha_ds.values.cost_time = round(time.time() - start_time, 5)
        setattr(alpha_ds.values, '%s_backtest' %self.sampling, 'Done')
        setattr(alpha_ds.values, '%s_cal_time' %self.sampling, str(datetime.now())[:19])
        return alpha_ds    
        









if __name__ == '__main__':
    w = AlphaCal(sampling='ALL')
    w.run()










