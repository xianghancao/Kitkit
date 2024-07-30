# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .talib_func import *
from .decorator import *

def drawdown(x):
    def func(cpnl):
        _cpnl = cpnl * np.ones((cpnl.shape[0], cpnl.shape[0]))
        _cpnl = np.tril(_cpnl)
        max_cpnl = np.nanmax(_cpnl, axis=1)
        return cpnl - max_cpnl
    res = np.zeros(x.shape) * np.nan
    for i in range(x.shape[1]):
        res[:,i] = func(x[:, i])
    return res



def drawdown_period(x):
    def func(cpnl):
        _cpnl = cpnl * np.ones((cpnl.shape[0], cpnl.shape[0]))
        _cpnl = np.tril(_cpnl)
        _cpnl = np.hstack((np.zeros((cpnl.shape[0],1)), _cpnl))
        max_cpnl = np.argmax(_cpnl, axis=1)
        return np.arange(len(cpnl)) - max_cpnl + 1
    res = np.zeros(x.shape)*np.nan
    for i in range(x.shape[1]):
        res[:, i] = func(x[:,i])
    return res


def scale_one(x):
    #归一化处理
    x[np.isinf(x)] = np.nan
    res = (x.T / (np.nansum(np.abs(x), axis=1) + 1e-20)).T
    return res


def equal_wgts(x):
    x = np.nan_to_num(x)
    x[x > 0] = 1
    x[x < 0] = -1
    return x