

# encoding: utf-8
import numpy as np
import pandas as pd

class CloseDeal():
    def __init__(self, data, alpha, maxlookback, 
                    quintiles=3, cost=0.):
        self.OpenPrice = data.OpenPrice
        self.ClosePrice = data.ClosePrice
        self.dates = data.dates
        self.idx = np.arange(maxlookback, len(data.dates))
        self.alpha = alpha


    def build(self):
        self.deal()
        self.scale_one()


    def deal(self):
        """
                        -----------------------------------------------------------------------------
        time                |...|         idx-1         |         idx          |       idx+1        |
                        -----------------------------------------------------------------------------
                            |   |                       |      dates           |                    |
                        -----------------------------------------------------------------------------
        alpha               |...|        alpha          |                      |       ...          |
                        -----------------------------------------------------------------------------
        Openprice trade     |...|                       |      OpenPrice       |     post_open      |
                        -----------------------------------------------------------------------------
        ClosePrice trade    |...|       ClosePrice      |      post_close      |       ...          |  
                        -----------------------------------------------------------------------------
        """
        
        self.resample_dates = self.dates[self.idx]

        self.resample_wgts = self.alpha[self.idx-1]                                     # 交易日使用的权重

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


