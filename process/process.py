# encoding: utf-8
import numpy as np
import pandas as pd

class Process():
    def __init__(self, data, alpha, maxlookback, deal_type=1,
                    quintiles=3, cost=0.):
        self.OpenPrice = data.OpenPrice
        self.ClosePrice = data.ClosePrice
        self.dates = data.dates
        self.idx = np.arange(maxlookback, len(data.dates))
        self.alpha = alpha
        self.deal_type = deal_type

    def build(self):
        self.deal()
        self.scale_one()


    def deal(self):
        # 在回测区间内，按照指定的Cycle和T+N进行重采样




        # cautious! 权重采样的同时，对于收盘价和开盘价进行采样
        """
                    -----------------------------------------------------------------------
        交易时间点  |...|         idx-1         |         idx          |       idx+1        |
                    -----------------------------------------------------------------------
                    |  |                        |      dates           |                |
                    ----------------------------------------------------------------------
        因子值      |...|        factor         |                      |       ...        |
                    -----------------------------------------------------------------------
        开盘价成交  |...|                       |      OpenPrice       |     post_open    |
                    -----------------------------------------------------------------------
        收盘价成交  |...|       ClosePrice      |      post_close      |       ...        |  
                    -----------------------------------------------------------------------
        """
        
        self.resample_dates = self.dates[self.idx]

        self.resample_wgts = self.alpha[self.idx-1]                                     # 交易日使用的权重
        
        # 1 按照开盘价成交
        if self.deal_type == 1:
            #self.OpenPrice[~self.TradeStatus] = np.nan
            OpenPrice = pd.DataFrame(self.OpenPrice).fillna(method='ffill').values
            OpenPrice = OpenPrice[self.idx]
            post_open = np.nan * np.zeros_like(OpenPrice)
            post_open[:-1] = OpenPrice[1:]
            #p_post_open = np.nan * np.zeros_like(OpenPrice)
            #p_post_open[:-1] = post_open[1:]
            self.resample_return = post_open/OpenPrice - 1
            self.resample_tradeprice = OpenPrice

        # 2 按照收盘价成交
        elif self.deal_type == 2: 
            #self.ClosePrice[~self.TradeStatus] = np.nan
            ClosePrice = pd.DataFrame(self.ClosePrice).fillna(method='ffill').values
            ClosePrice = ClosePrice[self.idx-1]
            post_close = np.nan * np.zeros_like(ClosePrice)
            post_close[:-1] = ClosePrice[1:]

            self.resample_return = post_close/ClosePrice - 1
            self.resample_tradeprice = ClosePrice


    def scale_one(self):
        # 
        self.resample_wgts[np.isinf(self.resample_wgts)] = np.nan
        self.scaled_resample_wgts = (self.resample_wgts.T / (np.nansum(np.abs(self.resample_wgts), axis=1) )).T


