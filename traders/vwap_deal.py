# encoding: utf-8
import numpy as np
import pandas as pd

class VWAPDeal():
    def __init__(self, data, alpha, maxlookback):
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
        VWAP trade          |...|                       |        VWAP          |     post_VWAP      |  
                        -----------------------------------------------------------------------------
        """
        
        self.resample_dates = self.dates[self.idx]
 
        self.resample_wgts = self.alpha[self.idx-1]                                     # 交易日使用的权重
        
        #self.OpenPrice[~self.TradeStatus] = np.nan
        VWAPPrice = pd.DataFrame(self.VWAPPrice).fillna(method='ffill').values
        VWAPPrice = VWAPPrice[self.idx]
        post_VWAP = np.nan * np.zeros_like(VWAPPrice)
        post_VWAP[:-1] = VWAPPrice[1:]

        self.resample_return = post_VWAP/VWAPPrice - 1
        self.resample_tradeprice = VWAPPrice



    def scale_one(self):
        # 
        self.resample_wgts[np.isinf(self.resample_wgts)] = np.nan
        self.scaled_resample_wgts = (self.resample_wgts.T / (np.nansum(np.abs(self.resample_wgts), axis=1) )).T


