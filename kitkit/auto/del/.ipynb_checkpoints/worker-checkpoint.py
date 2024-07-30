# coding=utf-8
# 20170426
import numpy as np
import pandas as pd
from munch import Munch
import json, os
from prob_engine import ProbEngine
from data_structure import DataStructure
from backtest import BackTest


def delay(x, period=1):
    """
    [Definition] 序列x中前period天的价格
    [Category] 技术指标
    delay() value of x d days ago
    """
    res = np.zeros(x.shape) * np.nan
    res[period:] = x[:-period]
    return res

"""
功能
- 计算表达式
- 初步回测信号，产生sharpe值，并存储

"""

class Worker():
    def __init__(self):
        self.prepare()



    def prepare(self):
        # 切割样本IS，OOS
        eod_path = 'eod'
        dates = np.load(os.path.join('/mnt/ssd/', eod_path, '1day/dates.npy'))
        idx = np.where(dates > '2016-03-30 09:00:00')[0][0]

        # 加载数据
        self.eod = Munch()
        self.eod.dates = dates[idx:]
        self.eod.ticker_names = np.load(os.path.join('/mnt/ssd/', eod_path, '1day/ticker_names.npy'))
        for i in ['OpenPrice', 'ClosePrice', 'HighestPrice', 'LowestPrice', 'Volume', 'VWAP', 'Position', 'TurnOver']:
            self.eod[i] = np.load(os.path.join('/mnt/ssd/', eod_path, i + '.npy')).T[idx:]
        self.eod.Ret = self.eod.Close*1./delay(self.eod.Close, 1) - 1

        self.resample_returns = pd.DataFrame((self.eod.OpenPrice.shift(-1)*1./self.eod.OpenPrice-1)[1:],
                                             index=self.eod.dates[1:],
                                             columns=self.eod.ticker_names)



    def cal_alphas(self, expr_ds):
        # 计算信号
        for i in ['OpenPrice', 'ClosePrice', 'HighestPrice', 'LowestPrice', 'Volume', 'VWAP', 'Position', 'TurnOver']:
            expr_tmp = expr_ds.values.expr.replace(i, 'self.eod.%s' %i)
        alphas = eval(expr_tmp)
        resample_wgts = pd.DataFrame(alphas[:-1] * 1., index=self.eod.dates[1:], columns=self.eod.ticker_names)
        bt = BackTest(resample_wgts, returns=self.resample_returns, cycle='day',
                    IS_OOS_ratio=None, stat_info=False, plot=False,
                    quintiles=3, turnover=1, cost=0., ticker_names=None,
                    output_dir=None, test_mode=False, signal_name=None)      
        bt.stat_quintiles()
        bt.stat_quintiles_pnl()
        bt.stat_alpha_pnl()
        bt.stat_alpha_sharpe()

        # 保存信号
        print expr_ds.values.id, expr_ds.values.expr, 'sharpe:', bt.alpha_sharpe
        #expr_ds.write(expr_ds.values.id)


if __name__ == '__main__':
    w = Worker()
    ds = DataStructure()
    ds.read('layer1', 'aae599d4-491e-11e8-8c43-801844e189f4')
    w.cal_alphas()


















