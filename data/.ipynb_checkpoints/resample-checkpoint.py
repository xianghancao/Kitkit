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
    def __init__(self, IS_start, IS_end, OOS_start=None, OOS_end=None, IS_OOS_ratio=None):
        self.IS_OOS_ratio = IS_OOS_ratio
        self.IS_start = IS_start #pd.to_datetime(str(IS_start))
        self.IS_end = IS_end #pd.to_datetime(str(IS_end))
        self.OOS_start = OOS_start#pd.to_datetime(str(OOS_start))
        self.OOS_end = OOS_end #pd.to_datetime(str(OOS_end))



    def build(self, Data):
        IS_Data = Object()
        OOS_Data = Object()

        if self.OOS_start is None and self.OOS_end is None and self.IS_OOS_ratio is None:
            is_index = np.where(Data.dates>=self.IS_start)[0][0]
            split_index = np.where(Data.dates>=self.IS_end)[0][-1]
            for i in get_elements(Data):
                setattr(IS_Data, i, getattr(Data, i)[is_index:split_index])
            print('[data][resample] IS start:%s end:%s' %(IS_Data.dates[0], IS_Data.dates[-1]))
            return IS_Data

        elif self.OOS_start is not None and self.OOS_end is not None and self.IS_OOS_ratio is None:
            is_index = np.where(Data.dates>=self.IS_start)[0][0]
            split_index = np.where(Data.dates<self.OOS_start)[0][-1]
            oos_index = np.where(Data.dates<self.OOS_end)[0][-1]
            for i in get_elements(Data):
                setattr(IS_Data, i, getattr(Data, i)[is_index:split_index])
                setattr(OOS_Data, i, getattr(Data, i)[split_index:oos_index])
            print('[data][resample] IS start:%s end:%s' %(IS_Data.dates[0], IS_Data.dates[-1]))
            print('[data][resample] OOS start:%s end:%s' %(OOS_Data.dates[0], OOS_Data.dates[-1]))
            return IS_Data, OOS_Data

        elif self.IS_OOS_ratio is not None:
            is_index = np.where(Data.dates>=self.IS_start)
            split_index = np.where(Data.dates<self.OOS_start)
            oss_index = np.where(Data.dates<self.OOS_end)
            IS_OOS_idx = int(len(Data.dates[is_index:oss_index])*self.IS_OOS_ratio)
            for i in get_elements(Data):
                setattr(IS_Data, i, getattr(Data, i)[s_index:e_index][:IS_OOS_idx])
                setattr(OOS_Data, i, getattr(Data, i)[s_index:e_index][IS_OOS_idx:])    
                              
            print('[data][resample] IS start:%s end:%s' %(IS_Data.dates[0], IS_Data.dates[-1]))
            print('[data][resample] OOS start:%s end:%s' %(OOS_Data.dates[0], OOS_Data.dates[-1]))

            return IS_Data, OOS_Data


