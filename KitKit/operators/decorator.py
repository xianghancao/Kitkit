# coding=utf-8
import pandas as pd
import numpy as np


def decorator(func):
    def wrapper(*args, **kw):
        # 判断ndarray or dataframe
        dataframe_lable = False
        _args = []
        for a in args:
            if isinstance(a, pd.DataFrame):
                index_val = a.index.values
                columns_val = a.columns.values
                dataframe_lable = True
                _args.append(a.values)
            else:
                _args.append(a)

        # 计算
        func_res = func(*_args, **kw)

        # dataframe还原
        if dataframe_lable:
            if len(func_res.shape) > 2:
                res_ = []
                for i in range(len(func_res)):
                    res_.append(pd.DataFrame(func_res[i, :], index=index_val, columns=columns_val))
            else:
                res_ = pd.DataFrame(func_res, index=index_val,columns=columns_val)
            return res_
        else:
            return func_res
    return wrapper