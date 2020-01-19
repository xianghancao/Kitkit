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
    def __init__(self, IS_start=None, IS_end=None, OOS_start=None, OOS_end=None, IS_OOS_ratio=None):
        self.IS_OOS_ratio = IS_OOS_ratio
        self.IS_start = IS_start #pd.to_datetime(str(IS_start))
        self.IS_end = IS_end #pd.to_datetime(str(IS_end))
        self.OOS_start = OOS_start#pd.to_datetime(str(OOS_start))
        self.OOS_end = OOS_end #pd.to_datetime(str(OOS_end))



    def build(self, Data):
        IS_Data = Object()
        OOS_Data = Object()
        if self.IS_start is not None and self.OOS_start is not None  and IS_OOS_ratio is None:
            is_index = np.where(Data.dates>=self.IS_start)
            split_index = np.where(Data.dates<self.OOS_start)
            oss_index = np.where(Data.dates<self.OOS_end)
            for i in get_elements(Data):
                setattr(IS_Data, i, getattr(Data, i)[is_index:split_index])
                setattr(OOS_Data, i, getattr(Data, i)[split_index:oss_index])

        elif self.IS_start is not None and self.OOS_end is not None and IS_OOS_ratio is not None:
            is_index = np.where(Data.dates>=self.IS_start)
            split_index = np.where(Data.dates<self.OOS_start)
            oss_index = np.where(Data.dates<self.OOS_end)
            IS_OOS_idx = int(len(Data.dates[is_index:oss_index])*self.IS_OOS_ratio)
            for i in get_elements(Data):
                setattr(IS_Data, i, getattr(Data, i)[s_index:e_index][:IS_OOS_idx])
                setattr(OOS_Data, i, getattr(Data, i)[s_index:e_index][IS_OOS_idx:])    
                              
        elif self.IS_OOS_ratio is not None:
            IS_OOS_idx = int(len(Data.dates)*self.IS_OOS_ratio)
        
            data_names = get_elements(Data)
            for i in data_names:
                setattr(IS_Data, i, getattr(Data, i)[:IS_OOS_idx])
                setattr(OOS_Data, i, getattr(Data, i)[IS_OOS_idx:])
        else:
            raise Exception('Pls set either of IS_start or IS_OOS_ratio')
        return IS_Data, OOS_Data


