# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .talib_func import *
from .decorator import *


@decorator
def sum(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求和
    [Category] 统计
    """
    if period > 1:
        return talib_func("SUM", x, timeperiod=period)
    elif period == 1:
        return x


@decorator
def ts_sum(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求和
    [Category] 统计
    """
    if period > 1:
        return talib_func("SUM", x, timeperiod=period)
    elif period == 1:
        return x



@decorator
def ts_product(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动平方加和
    [Category] 统计
    time-series product over the past period days
    """
    tmp = x ** 2
    if period > 1:
        return talib_func('SUM', tmp, timeperiod=period)
    elif period == 1:
        return tmp


@decorator
def ts_min(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求最小值
    [Category] 统计
    """
    # 取前n天数据的最小值
    return talib_func("MIN", x, timeperiod=period)


@decorator
def ts_max(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求最大值
    [Category] 统计
    """
    return talib_func("MAX", x, timeperiod=period)


# @decorator
# def ts_argmax(x, period):
#     """
#     [Definition] 对x中的每个时间序列在period范围内滚动求最大值的位置，过去period天的最大值的位置，范围[1,period]
#     [Category] 统计
#     """
#     res = - talib_func("MAXINDEX", x, timeperiod=period) + (np.arange(x.shape[0]) * np.ones_like(x).T).T 
#     #res[0:period - 1] = np.nan
#     #res = pd.rolling_apply(pd.DataFrame(x), window=period, func=np.argmax, min_periods=period, kwargs={'axis':0}).values
#     return res


@decorator
def ts_argmax(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求最大值的位置，过去period天的最大值的位置，范围[1,period]
    [Category] 统计
    """
    res=pd.DataFrame(x).notnull().cumsum().values-talib_func("MAXINDEX", x, timeperiod=period)-1
    res[0:period - 1] = np.nan
    res[np.isnan(x)] = np.nan
    return res


# @decorator
# def ts_argmin(x, period):
#     """
#     [Definition] 对x中的每个时间序列在period范围内滚动求最小值的位置，过去period天的最小值的位置，范围[1,period]
#     [Category] 统计

#     """
#     res = - talib_func("MININDEX", x, timeperiod=period) + (np.arange(x.shape[0]) * np.ones_like(x).T).T 
#     #res[0:period - 1] = np.nan
#     #res = pd.rolling_apply(pd.DataFrame(x), window=period, func=np.argmin, min_periods=period, kwargs={'axis':0}).values
#     return res


@decorator
def ts_argmin(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求最大值的位置，过去period天的最大值的位置，范围[1,period]
    [Category] 统计
    """
    res=pd.DataFrame(x).notnull().cumsum().values-talib_func("MININDEX", x, timeperiod=period)-1
    res[0:period - 1] = np.nan
    res[np.isnan(x)] = np.nan
    return res



@decorator
def rank(x):
    """
    [Definition] 对x进行空头和多头的横截面排序, 
    [Category] 统计
    这里需要注意，不能分别对多头和空头进行排序，不然会出现不对称性
    """
    tmp_x = x.copy() 
    idx = np.sum(~np.isnan(tmp_x), axis=1) == 0  #某行全为nan值

    tmp_x[idx, :] = 0
    sz = np.sum(~np.isnan(x), axis=1)
    res = (st.mstats.rankdata(tmp_x, axis=1).T/sz.astype(float)).T
    res[np.isnan(x)] = np.nan
    return res

    
@decorator
def ts_rank(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内进行滚动排序
    [Category] 统计
    st.mstats.rankdata算法太慢, 用np.argsort替代，需要改进
    """
    res = np.zeros(x.shape) * np.nan
    for ix in range(0, x.shape[0] - period + 1):
        res[ix + period - 1] = (np.argsort(np.argsort(x[ix:ix + period], axis=0), axis=0)[-1] + 1) * 1. / period
    res[np.isnan(x)] = np.nan
    return res


@decorator
def ma(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求均值
    [Category] 统计
    """
    res = talib_func("MA", x, timeperiod=period)
    return res


@decorator
def mean(x, period):
    """
    [Definition]对x中的每个时间序列在period范围内滚动求均值, 同ma
    [Category] 统计
    """
    res = talib_func("MA", x, timeperiod=period)
    return res



@decorator
def median(x, period):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求中位数
    [Category] 统计
    """
    pass
    # res = [np.nan] * (period - 1)
    # for i in range(len(x) - period + 1):
    #     res.append(np.nanmedian(x[i: i + period]))
    # return np.array(res)



@decorator
def percentile(x, period, percentile):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求分位数
    [Category] 统计
    """
    pass
    # res = [np.nan] * (period - 1)
    # for i in range(len(x) - period + 1):
    #     res.append(np.nanpercentile(x[i: i + period], percentile))
    # return np.array(res)



@decorator
def skewness(x, period):
    """
    [Definition] 序列x的前period日偏度值
    [Category] 统计
    """
    res = np.zeros_like(x) * np.nan
    for i in range(x.shape[1]):
        idx = np.isnan(x[:,i])
        res[:,i][~idx] = pd.DataFrame(x[:,i][~idx]).rolling(period).skew().iloc[:,0].values
    return res


@decorator
def kurtosis(x, period):
    """
    [Definition] 序列x的前period日峰度值
    [Category] 统计
    return the rolling kurtosis of x
    nan_policy: decide how to handle when input contains nan.
                'omit' performs the calculations ignoring nan values.
                Default is 'propagate' that will let kurtosis return nan
    for details:http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html
    """
    res = np.zeros_like(x) * np.nan
    for i in range(x.shape[1]):
        idx = np.isnan(x[:,i])
        res[:,i][~idx] = pd.DataFrame(x[:,i][~idx]).rolling(period).kurt().iloc[:,0].values
    return res


@decorator
def k_moment(x, period, pow=2):  
    """
    [Definition] 序列x前period日的滚动k阶中心距
    [Category] 统计
    计算x的滚动k阶中心距
    """
    import scipy.stats as st
    def moment(x):
        return st.moment(x, moment=pow, nan_policy='omit')

    res = np.zeros_like(x) * np.nan
    for i in range(x.shape[1]):
        idx = np.isnan(x[:,i])
        res[:,i][~idx] = pd.DataFrame(x[:,i][~idx]).rolling(period).apply(moment).iloc[:,0].values
    return np.array(res)


@decorator
def geometric_mean(x):
    """
    [Definition] 序列x的滚动几何平均数, [sqrt(x1*x2), sqrt(x2*x3), …… , sqrt(xn-1*xn)], Notes:the first element is nan
    [Category] 特殊符号函数
    """
    x_shift = np.zeros_like(x) * np.nan
    x_shift[: -1] = x[1:]
    x_roll = x * x_shift
    x_roll[1:] = x_roll[: -1]
    x_roll[0] = np.nan
    return np.sqrt(x_roll)


@decorator
def beta(high, low, period):
    """
    [Definition] CAPM模型中的beta系数
    [Category] 统计
    """
    return talib_func('BETA', high, low, timeperiod=period)


@decorator
def linearreg(data, period):
    """
    [Definition] 线性回归
    [Category] 统计
    """
    return talib_func('LINEARREG', data, timeperiod=period)


@decorator
def linearreg_angle(data, period):
    """
    [Definition] 线性回归的一种最小角回归，主要针对解决高维回归问题
    [Category] 统计
    """

    return talib_func('LINEARREG_ANGLE', data, timeperiod=period)


@decorator
def linearreg_intercept(data, period):
    """
    [Definition] 回归的截距
    [Category] 统计
    """
    return talib_func('LINEARREG_INTERCEPT', data, timeperiod=period)


@decorator
def linearreg_slope(data, period):
    """
    [Definition] 线性回归的斜率
    [Category] 统计
    """
    return talib_func('LINEARREG_SLOPE', data, timeperiod=period)


@decorator
def tsf(data, period):
    """
    [Definition] 时间序列预测
    [Category] 统计
    """
    return talib_func('TSF', data, timeperiod=period)


@decorator
def stddev(x, period):  # 标准差
    """
    [Definition] 序列x在前period日的标准差
    [Category] 统计
    """
    return talib_func('STDDEV', x, timeperiod=period)


@decorator
def var(data, period):
    """  
    [Definition] 序列x在前period日的方差
    [Category] 统计
    """
    return talib_func('VAR', data, timeperiod=period)


@decorator
def scale(x):  # 缩放运算
    """
    [Definition] 序列x的归一化，数据在（-1,1）之间
    [Category] 统计
    rescaled x such that sum(abs(x)) = a (the default is a = 1)
    """
    res = (x.T / (np.nansum(np.abs(x), axis=1) + 1e-20)).T
    return res


@decorator
def correlation(x, y, period):
    """
    [Definition] 序列x和y在前period日的皮尔逊相关系数
    [Category] 统计
    """
    return talib_func('CORREL', x, y, timeperiod=period)


@decorator
def covariance(x, y, period):
    """
    [Definition] 序列x和y在前period日的协方差,使用皮尔森相关系数的公式算协方差公式
    [Category] 统计
    """
    corr_matrix = talib_func('CORREL', x, y, timeperiod=period)
    var_x = talib_func('VAR', x, timeperiod=period)
    var_y = talib_func('VAR', y, timeperiod=period)
    return corr_matrix * var_x * var_y




@decorator
def count_nans(x, period):
    """
    [Definition] 最近period周期内序列x中NAN元素的个数
    [Category] 统计

    return the number of NANs in x during last period
    """
    return ts_sum(1.*np.isnan(x), period)
    

@decorator
def ts_count(cond, period):
    """
    [Definition] 最近period周期内序列x中满足cond的元素个数
    [Category] 统计
    return the number of cond=True in x during last period
    """
    return talib_func("SUM", 1.*(cond==True), timeperiod=period)




if __name__ == '__main__':
    test_arr = np.arange(99).reshape(33,3)
    test_arr[5,0] = np.nan
    ts_rank(test_arr, 6)


