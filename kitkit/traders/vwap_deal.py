# encoding: utf-8
import numpy as np
import pandas as pd

class VWAPDeal():
    def __init__(self, data, alpha, maxlookback):
        self.VWAP = data.VWAP
        self.OpenPrice = data.OpenPrice
        self.ClosePrice = data.ClosePrice
        self.dates = data.dates
        self.TradeStatus = data.TradeStatus
        self.Volume = data.Volume
        self.idx = np.arange(maxlookback, len(data.dates))
        self.alpha = alpha
        print('[Traders][vwap_deal] maxlookback:%s' %maxlookback)

    def build(self):
        self.trade_check()
        self.volume_check()
        self.deal()
        self.scale_one()

    def trade_check(self):
        """
        交易状态为False，禁止买入卖空
        """
        self.alpha[~self.TradeStatus] = np.nan
    
    def volume_check(self):
        """
        无成交量，禁止买入卖空
        """
        self.alpha[self.Volume == 0.] = np.nan
        self.alpha[np.isnan(self.Volume)] = np.nan
        

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
        VWAPPrice = pd.DataFrame(self.VWAP).fillna(method='ffill').values
        VWAPPrice = VWAPPrice[self.idx]
        post_VWAP = np.nan * np.zeros_like(VWAPPrice)
        post_VWAP[:-1] = VWAPPrice[1:]

        self.resample_return = post_VWAP/VWAPPrice - 1
        self.resample_tradeprice = VWAPPrice



    def scale_one(self):
        # 
        self.resample_wgts[np.isinf(self.resample_wgts)] = np.nan
        self.resample_wgts[np.logical_and(self.resample_wgts<1e-10, self.resample_wgts>-1e-10)] = 0
        self.scaled_resample_wgts = (self.resample_wgts.T / (np.nansum(np.abs(self.resample_wgts), axis=1) )).T


