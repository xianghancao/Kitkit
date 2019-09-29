# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .function_wrapper import *
from .decorator import *

@decorator
def decay_linear(x, period):
    """
    [Definition] 序列x的前period日权重滑动平均线(WMA)，较近日期权重较高，较远日期千重较低, weighted moving average over the past d days with linearly decaying  weights d, d – 1, …, 1 (rescaled to sum up to 1)
    [Category] 信号处理
    """
    return function_wrapper("WMA", x, timeperiod=period)


# @decorator
# def decay_exponent(x, period):
#     """
#     [Definition] 序列x的前period日指数滑动平均线(EMA), exponential moving average over the past d days with exponent decaying  weights d, d – 1, …, 1 (rescaled to sum up to 1)
#     [Category] 信号处理
#     """
#     return function_wrapper("EMA", x, timeperiod=period)


# @decorator
# def decay_fibonacci(x, period):
#     """
#     [Definition] 序列x的前period日权重滑动滚动加权平均线，加权系数为菲波那切数列, rolling fibonacci-number weighted
#     [Category] 信号处理
#     """
#     def fib_number(n):
#         a, b = 0, 1
#         for i in range(n):
#             a, b = b, a + b
#         return a

#     fibonacci = []
#     for j in range(period):
#         fibonacci.append(fib_number(j + 1))
#     fibonacci = np.array(fibonacci)
#     weight = fibonacci / (np.nansum(np.abs(fibonacci)) + 0.0)
#     res = [np.nan] * (period - 1)
#     l = len(x)
#     for i in range(l - period + 1):
#         res.append((x[i: i + period] * weight).sum())
#     return np.array(res)
