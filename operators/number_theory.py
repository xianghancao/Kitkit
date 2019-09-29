# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .function_wrapper import *
from .decorator import *

# ====================================数论====================================
@decorator
def factorial(x):
    """
    [Definition] 对x做阶乘，return each element's factorial of x，x: 1-dimension ndarray
    [Category] 数论
    """
    try:
        from math import factorial as fa
    except:
        raise Exception('can not import math.factorial() in function factorial()!')
    res = np.zeros_like(x) * np.nan
    for i in range(len(x)):
        res[i] = fa(x[i])
    return res


@decorator
def ceil(x):
    """
    [Definition] 对x向上取整，return smallest integer larger than x
    [Category] 数论
    '"""
    return np.ceil(x)


@decorator
def floor(x):
    """
    [Definition] 对x向下取整，return largest integer less than x
    [Category] 数论
    """
    return np.floor(x)



@decorator
def reciprocal(x):
    """
    [Definition] 对x取倒数
    [Category] 数论
    """
    if ~x.all():
        raise Exception('INFs exist in function reciprocal()!')
    return 1.0 / x

