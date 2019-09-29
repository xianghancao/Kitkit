# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .function_wrapper import *
from .decorator import *

# ====================================预处理====================================
@decorator
def pasteurize(x):
    """
    [Definition] 奇异值处理为NAN，set to Nan if it is INF
    [Category] 预处理
    """
    res = x.copy()
    res[np.isinf(x)] = np.nan
    return res
    

@decorator
def universe_process(x, universe_t_f):
    """
    [Definition] 选股池，set to Nan if the underlying instrument is not in the universe
    [Category] 预处理
    """
    pass


@decorator
def indneutralize(x, industry):
    """
    [Definition] 行业中性化
    [Category] 预处理
    """
    pass


@decorator
def ffill(x):
    """
    [Definition] 向前填充
    [Category] 预处理
    """
    return pd.DataFrame(x).fillna(method='ffill').values