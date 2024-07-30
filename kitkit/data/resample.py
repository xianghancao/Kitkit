# coding=utf-8
import numpy as np
import pandas as pd
import inspect

class Object():
    pass

def get_elements(obj, remove_default=True):
    ins = inspect.getmembers(obj)
    for i in ins:
        if i[0] == '__dict__':
            return i[1]['data_names']


class Resample():
    def __init__(self, IS_start, IS_end, OOS_start=None, OOS_end=None, IS_OOS_ratio=None, tickers=None):
        self.IS_OOS_ratio = IS_OOS_ratio
        self.IS_start = IS_start #pd.to_datetime(str(IS_start))
        self.IS_end = IS_end #pd.to_datetime(str(IS_end))
        self.OOS_start = OOS_start#pd.to_datetime(str(OOS_start))
        self.OOS_end = OOS_end #pd.to_datetime(str(OOS_end))
        self.tickers = tickers


    def build(self, Data):
        IS_Data = Object()
        OOS_Data = Object()
        if self.tickers is None:
            self.tickers = Data.ticker_names
            
        idx = np.in1d(Data.ticker_names, self.tickers)
        if self.OOS_start is  None or self.OOS_end is  None:
            is_start_index = np.where(Data.dates>=self.IS_start)[0][0]
            is_end_index = np.where(Data.dates<self.IS_end)[0][-1]
            for i in get_elements(Data):
                if i == 'ticker_names':
                    IS_Data.ticker_names = Data.ticker_names[idx]
                    continue
                if i == 'dates':
                    IS_Data.dates = Data.dates[is_start_index:is_end_index]
                    continue
                setattr(IS_Data, i, getattr(Data, i)[is_start_index:is_end_index][:, idx])
            print('[data][resample] IS start:%s end:%s' %(IS_Data.dates[0], IS_Data.dates[-1]))
            print('[data][resample] tickers quantity: %s' %len(IS_Data.ticker_names))
            return IS_Data, OOS_Data

        elif self.OOS_start is not None and self.OOS_end is not None: 

            #elif self.OOS_start is not None and self.OOS_end is not None and self.IS_OOS_ratio is None:
            is_start_index = np.where(Data.dates>=self.IS_start)[0][0]
            is_end_index = np.where(Data.dates<self.IS_end)[0][-1]
            oos_start_index = np.where(Data.dates>=self.OOS_start)[0][0]
            oos_end_index = np.where(Data.dates<self.OOS_end)[0][-1]
            for i in get_elements(Data):
                if i == 'ticker_names':
                    IS_Data.ticker_names = Data.ticker_names[idx]
                    OOS_Data.ticker_names = Data.ticker_names[idx]
                    continue
                if i == 'dates':
                    IS_Data.dates = Data.dates[is_start_index:is_end_index]
                    OOS_Data.dates = Data.dates[oos_start_index:oos_end_index]
                    continue
                setattr(IS_Data, i, getattr(Data, i)[is_start_index:is_end_index][:, idx])
                setattr(OOS_Data, i, getattr(Data, i)[oos_start_index:oos_end_index][:, idx])
            print('[data][resample] IS start:%s end:%s' %(IS_Data.dates[0], IS_Data.dates[-1]))
            print('[data][resample] OOS start:%s end:%s' %(OOS_Data.dates[0], OOS_Data.dates[-1]))
            print('[data][resample] tickers quantity: %s' %len(IS_Data.ticker_names))
            return IS_Data, OOS_Data

            # elif self.IS_OOS_ratio is not None:
            #     is_index = np.where(Data.dates>=self.IS_start)
            #     split_index = np.where(Data.dates<self.OOS_start)
            #     oss_index = np.where(Data.dates<self.OOS_end)
            #     IS_OOS_idx = int(len(Data.dates[is_index:oss_index])*self.IS_OOS_ratio)
            #     for i in get_elements(Data):
            #         if i == 'ticker_names':
            #             IS_Data.ticker_names = Data.ticker_names[idx]
            #             OOS_Data.ticker_names = Data.ticker_names[idx]
            #             continue
            #         setattr(IS_Data, i, getattr(Data, i)[s_index:e_index][:IS_OOS_idx][:, idx])
            #         setattr(OOS_Data, i, getattr(Data, i)[s_index:e_index][IS_OOS_idx:][:, idx])    
                                  
            #     print('[data][resample] IS start:%s end:%s' %(IS_Data.dates[0], IS_Data.dates[-1]))
            #     print('[data][resample] OOS start:%s end:%s' %(OOS_Data.dates[0], OOS_Data.dates[-1]))

            #     return IS_Data, OOS_Data


