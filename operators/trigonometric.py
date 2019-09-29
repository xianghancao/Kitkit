# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .function_wrapper import *
from .decorator import *


# ====================================三角函数====================================
@decorator
def sin(x):
    """
    [Definition] x的正弦函数
    [Category] 三角函数
    """
    return np.sin(x)


@decorator
def cos(x):
    """
    [Definition] x的余弦函数
    [Category] 三角函数
    """
    return np.cos(x)


@decorator
def tan(x):
    """
    [Definition] x的正切函数
    [Category] 三角函数
    Notes:np.nan seems not to check domain of definition!
    """
    return np.tan(x)


# ====================================反三角函数====================================


@decorator
def arcsin(x):
    """
    [Definition] x的反正弦函数
    [Category] 反三角函数
    """
    # if ~(np.array(np.abs(x) <= 1)).all():
    #   raise OpException('NANs exist in function arcsin()!')
    return np.arcsin(x)


@decorator
def arccos(x):
    """
    [Definition] x的反余弦函数
    [Category] 反三角函数
    """
    # if ~(np.array(np.abs(x) <= 1)).all():
    #   raise OpException('NANs exist in functoin arccos()!')
    return np.arccos(x)


@decorator
def arctan(x):
    """
    [Definition] x的反正切函数
    [Category] 反三角函数
    """
    return np.arctan(x)


# ====================================双曲函数====================================


@decorator
def sinh(x):
    """
    [Definition] x的双曲正弦函数
    [Category] 双曲函数
    sinh = (e^x - e^-x) / 2
    """
    return np.sinh(x)


@decorator
def cosh(x):
    """
    [Definition] x的双曲余弦函数
    [Category] 双曲函数
    cosh = (e^x + e^-x) / 2
    """
    return np.cosh(x)


@decorator
def tanh(x):
    """
    [Definition] x的双曲正切函数
    [Category] 双曲函数
    tanh = (e^x - e^-x) / (e^x + e^-x)
    """
    return np.tanh(x)


# ====================================反双曲函数====================================


@decorator
def arcsinh(x):
    """
    [Definition] x的反双曲正弦函数
    [Category] 反双曲函数
    domain of definition: R
    """
    return np.arcsinh(x)


@decorator
def arccosh(x):
    """
    [Definition] x的反双曲余弦函数
    [Category] 反双曲函数
    domain of definition: [1, +Inf]
    """
    # if ~(np.array(x >= 1)).all():
    #   raise OpException('Warning: NANs exist in function arccosh()!')
    return np.arccosh(x)


@decorator
def arctanh(x):
    """
    [Definition] x的反双曲正切函数
    [Category] 反双曲函数
    domain of definition: (-1, 1)
    """
    # if ~(np.array(np.abs(x) < 1)).all():
    #   raise OpException('Warning: NANs exist in function arctanh()!')
    return np.arctanh(x)
