# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .function_wrapper import *
from .decorator import *

# ====================================元素级====================================
@decorator
def abs(x):
    """
    [Definition] 对x取绝对值
    [Category] 元素级
    """
    return np.abs(x)


@decorator
def sqrt(x):
    """
    [Definition] 对x开方
    [Category] 元素级
    """
    # if ~np.array((x >= 0)).all():
    #   raise OpException('NANs exist in function sqrt()!')
    return np.sqrt(x)


@decorator
def square(x):
    """
    [Definition] 对x平方
    [Category] 元素级
    """
    return np.square(x)


@decorator
def exp(x):
    """
    [Definition] 对x做指数运算
    [Category] 元素级
    """
    return np.exp(x)


@decorator
def log(x):
    """
    [Definition] 对x做对数运算
    [Category] 元素级
    """

    # if ~np.array((x > 0)).all():

    # raise OpException('NANs exist in function log()!')
    return np.log(x)


@decorator
def log10(x):
    """
    [Definition] 对x做以10为低的对数运算
    [Category] 元素级
    """
    # if ~np.array((x > 0)).all():
    #   raise OpException('NANs exist in function log10()!')
    return np.log10(x)


@decorator
def log2(x):
    """
    [Definition] 对x做以2为低的对数运算
    [Category] 元素级
    """
    # if ~np.array((x > 0)).all():
    #   raise OpException('NANs exist in function log2()!')
    return np.log2(x)


@decorator
def sign(x):
    """
    [Definition] x<0 返回-1；x>0 返回1； x==0 返回0
    [Category] 元素级
    """
    return np.sign(x)


@decorator
def signedpower(x, pow):
    """
    [Definition] 对x的绝对值做pow次方，并保存x的符号
    [Category] 元素级
    带符号的power
    """
    return np.power(np.abs(x), pow) * np.sign(x)



@decorator
def INTPART(x):
    """
    [Definition] 沿A绝对值减小方向最接近的取整
    [Category] 元素级
    """
    # 取整
    # 用法:INTPART(A)返回沿A绝对值减小方向最接近的整数
    # 例如:INTPART(12.3)求得12,INTPART(-3.5)求得-3
    import math
    def intpart(x):
        if x<0:
            return math.ceil(x)
        else:
            return math.floor(x)
    return np.array(map(intpart, x))


@decorator
def sigmoid(x):
    """
    [Definition] 序列x的S型生长曲线
    [Category] 特殊符号函数
    """
    return 1.0 / (1 + np.exp(-x))


@decorator
def nike(x):
    """
    [Definition] 序列x的对勾函数
    [Category] 特殊符号函数
    """
    # if ~x.all():
    #   raise Exception('INFs exist in function nike()!')
    return x + 1.0 / x
