# coding=utf-8
import numpy as np
from .talib_func import *
from .decorator import *

#====================================逻辑====================================
@decorator
def cond_expr(cond, expr1, expr2):
    '''
    [Definition] 如果cond成立，则为expr1，否则为expr2，cond? expr1: expr2，cond is a matrix with True or False in each postion
    [Category] 逻辑
    '''
    if np.isnan(expr1).all() or np.isnan(expr2).all():
        raise Exception('input argument should not be nan')
    res = cond*expr1 + ~cond*expr2
    return res


@decorator
def where(cond, expr1, expr2):
    '''
    [Definition] 如果cond成立，则为expr1，否则为expr2，cond? expr1: expr2，cond is a matrix with True or False in each postion
    [Category] 逻辑
    '''
    if np.isnan(expr1).all() or np.isnan(expr2).all():
        raise Exception('input argument should not be nan')
    res = cond*expr1 + ~cond*expr2
    return res



@decorator
def iff(cond, expr1, expr2):
    '''
    [Definition] 如果cond成立，则为expr1，否则为expr2，cond? expr1: expr2，cond is a matrix with True or False in each postion
    [Category] 逻辑
    '''
    if np.isnan(expr1).all() or np.isnan(expr2).all():
        raise Exception('input argument should not be nan')
    res = cond*expr1 + ~cond*expr2
    return res


    
@decorator
def or_expr(expr1, expr2):
    """
    [Definition] expr1和expr2逻辑运算
    [Category] 逻辑

    """
    return np.logical_or(expr1, expr2)


@decorator
def max(x, y):
    """
    [Definition] x和y对应位置元素比大小，取最大值
    [Category] 逻辑
    """
    if isinstance(x, int):
        x = np.ones_like(y)
    elif isinstance(y, int):
        y = np.ones_like(x)
    return x*(x>=y) + y*(x<y)


@decorator
def min(x, y):
    """
    [Definition] x和y对应位置元素比大小，取最小值
    [Category] 逻辑
    """
    if isinstance(x, int):
        x = np.ones_like(y)
    elif isinstance(y, int):
        y = np.ones_like(x)
    return x*(x<=y) + y*(x>y)


@decorator
def tail(x, lower, upper, newval):
    """
    [Definition] 如果x在区中（lower，upper）中时，重新赋值为newval
    [Category] 逻辑
    """
    # Set the values of x to newval if they are between lower and upper  
    cond =  (x < upper) * (x > lower) 
    return ~cond * x + newval