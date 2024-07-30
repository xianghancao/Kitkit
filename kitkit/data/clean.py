# coding=utf-8
import numpy as np
import pandas as pd
import os
import inspect

class Object():
    pass

def get_elements(obj, remove_default=True):
    ins = inspect.getmembers(obj)
    for i in ins:
        if i[0] == '__dict__':
            return i[1]

class Clean():
    def __init__(self):
        pass


    def build(self, dataObj):
        return self.fillna(dataObj)



    def fillna(self, dataObj, method='ffill'):
        print('[Data][Clean] fillna:%s' %method)
        fillna_data = Object()
        for i in get_elements(dataObj):
            if i == 'dates' or i=='ticker_names':
                setattr(fillna_data, i,  getattr(dataObj, i))
                continue
            #print(pd.DataFrame(getattr(dataObj, i)).fillna(method=method).values)
            setattr(fillna_data, i, pd.DataFrame(getattr(dataObj, i)).fillna(method=method).values)
        return fillna_data

