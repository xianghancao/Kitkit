# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .function_wrapper import *
from .decorator import *

@decorator
def sequence(n):
    """
    [Definition] 生成值为1到n的数组
    [Category] 其他
    """
    return np.arange(1, n+1)