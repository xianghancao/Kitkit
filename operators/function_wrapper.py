# coding=utf-8
# 20180427
import numpy as np
import talib
import pandas as pd


# =======================  new function_wrapper =========================

def function_wrapper(func, *args, **kwargs):
   

    func = func.upper()

    for a in args:
        if isinstance(a, np.ndarray):
            s = a.shape
    res = np.zeros(s,).astype(np.float) * np.nan

    if func in getattr(talib.func, '__TA_FUNCTION_NAMES__'):
        f = getattr(talib, func)
    else:
        raise Exception("%s is not a valid talib function" % func)

    for i in range(s[-1]):
        one_dim_args = []
        nan_df = pd.DataFrame()
        #20171116 剔除nan值, 特别是correlation这类运算符
        for a in args:
            nan_df = nan_df.append(pd.DataFrame(np.isnan(a[:,i])).T)
        not_nan = (nan_df.sum(axis=0) == 0).values

        for a in args:
            if isinstance(a, np.ndarray) and a.shape == s:
                al = a[:, i]
                one_dim_args.append(al[not_nan])  
            else:
                one_dim_args.append(a)
        
        ri = f(*one_dim_args,**kwargs)
        
        if isinstance(ri, tuple):
            if i==0:
                sl = list(s)
                sl.insert(0,len(ri))
                res = np.zeros(tuple(sl),dtype=float) * np.nan
            for q in range(len(ri)):
                res[q,:,i][not_nan] = ri[q]
        else:
            res[:,i][not_nan] = ri

    return res


# def apply_func_old(func, *args, **kwargs):
   
#     s = tuple()
#     for a in args:
#         if isinstance(a, np.ndarray):
#             s = a.shape

#     res = np.zeros(s,).astype(np.float)
#     #f_l = func.lower()
#     func = func.upper()

#     if func in talib.func.__all__:
#         f = getattr(talib, func)
#     else:
#         raise Exception("%s is not a valid talib function" % func)

#     for i in range(s[-1]):
#         one_dim_args = []
#         for a in args:
#             if isinstance(a, np.ndarray) and a.shape == s:
#                 #a = np.nan_to_num(a)
#                 al = a[:,i]
                
#                 # Talib functions can not handle input with all element is np.nan
#                 # So give a 0
#                 if np.all(np.isnan(al)):
#                     al[0] = 0

#                 # old
#                 al = np.nan_to_num(al)

#                 one_dim_args.append(al)
#             else:
#                 one_dim_args.append(a)
         
#         ri = f(*one_dim_args,**kwargs)
        
#         if isinstance(ri, tuple):
#             if i==0:
#                 sl = list(s)
#                 sl.insert(0,len(ri))
#                 res = np.zeros(tuple(sl),dtype=float)
#             for q in range(len(ri)):
#                 res[q,:,i] = ri[q]
#         else:
#             res[:,i] = ri
#     return res


# def function_wrapper(func, *args, **kwargs):
#     func = func.upper()
#     res = apply_func_old(func, *args, **kwargs)
#     return res
