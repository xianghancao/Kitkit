# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .function_wrapper import *
from .decorator import *


# ====================================复杂表达式====================================
@decorator
def sum_i(expr_str, var_str, start, stop, step):
    """
    [Definition] 连续求和expr_str(i)*i，其中i属于（start，stop，step），loop over var(from start to stop with step) and calculate expr at every iteration (presumably expr would contain var), then sum over all the values.
    e.g. sum_i(delay(c, i)*i, i, 2, 4, 1) would be equivalent to delay(c, 2) *2 + delay(c, 3)*3 +delay(close, 4) *4
    [Category] 复杂运算符

    """
    space = np.arange(start, stop, step)
    res = []
    for i in space:
        if len(res) == 0:
            res = eval(expr_str.replace(var_str, i))
        else:
            res += eval(expr_str.replace(var_str, i))
    return res

    
@decorator
def call_i(expr_str, var_str, subexpr):
    """
    [Definition] call_i(x+4, x, 2+3) would be equivalent to (2+3)+4
    [Category] 复杂运算符
    """
    return eval(expr_str.replace(var_str, str(subexpr)))