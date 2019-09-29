# coding=utf-8
import numpy as np
import scipy.stats as st
import talib
import pandas as pd
from .function_wrapper import *
from .decorator import *
from statistics import *

@decorator
def delay(x, period=1):
    """
    [Definition] 序列x中前period天的价格
    [Category] 技术指标
    delay() value of x d days ago
    """
    res = np.zeros(x.shape) * np.nan
    for i in range(x.shape[1]):
        nan_dix = np.isnan(x[:, i])
        nan_arr = x[:, i][~nan_dix]
        delay_nan_arr  = np.zeros(nan_arr.shape) * np.nan
        delay_nan_arr[period:] = nan_arr[:-period]
        res[~nan_dix, i] = delay_nan_arr
    return res


@decorator
def delta(x, period):
    """
    [Definition] 间隔period时间的一阶差分
    [Category] 技术指标
    today’s value of x minus the value of x d days ago
    """
    return x - delay(x, period)


@decorator
def delta2(x, period1, period2):
    """
    [Definition] 间隔period时间的二阶差分
    [Category] 技术指标
    x的二阶差分
    """
    return delta(delta(x, period1), period2)


# ====================================Technical====================================

@decorator
def llv(data, n):
    """
    [Definition] 数据在n天内的最低价值
    [Category] 技术指标
    """
    return function_wrapper("MIN", data, timeperiod=n)

@decorator
def hhv(data, n):
    """
    [Definition] 数据在n天内的最高价值
    [Category] 技术指标
    """
    return function_wrapper("MAX", data, timeperiod=n)


@decorator
def atr(high, low, close, period):
    """
    [Definition] 数据在n天内平均波动范围
    [Category] 技术指标
    """
    return function_wrapper('ATR', high, low, close, timeperiod=period)


@decorator
def atr_rate(high, low, close, period):
    """
    [Definition] 数据在n天内平均波动率
    [Category] 技术指标
    """
    return function_wrapper('ATR', high, low, close, timeperiod=period) / close


@decorator
def sub(high, low):
    """
    [Definition] 当日的最大价格差
    [Category] 技术指标
    """
    return function_wrapper('SUB', high, low)


@decorator
def ht_trendline(data):
    """
    [Definition] 希尔伯特变换-趋势vs周期模式
    [Category] 技术指标
    """
    return function_wrapper('HT_TRENDLINE', data)


@decorator
def kama(data, period):
    
    """
    [Definition] 以period为周期的考夫曼自适应移动平均线
    [Category] 技术指标
    """
    return function_wrapper('KAMA', data, timeperiod=period)


@decorator
def midpoint(data, period):
    """
    [Definition] (highest value-lowest value)/2k
    [Category] 技术指标
    """
    return function_wrapper('MIDPOINT', data, timeperiod=period)


@decorator
def ema(data, period):
    """
    [Definition] 以period为周期的指数加权移动平均线
    [Category] 技术指标
    """
    return function_wrapper('EMA', data, timeperiod=period)


@decorator
def wma(data, period):
    """
    [Definition] 以period为周期的加权移动平均线
    [Category] 技术指标
    """
    return function_wrapper('WMA', data, timeperiod=period)


@decorator
def tema(data, period):
    """
    [Definition] 以period为周期的三指数移动平均线
    [Category] 技术指标
    """
    return function_wrapper('TEMA', data, timeperiod=period)


@decorator
def macd(close, short=12, long=26, mid=9):
    """
    [Definition] 平滑异同移动平均线
    [Category] 技术指标
    """
    dif = ema(close, short) - ema(close, long)
    dea = ema(dif, mid)
    macd = (dif - dea) * 2
    return macd


@decorator
def kdj(close, high, low, n=9, m1=3, m2=3):
    """
    [Definition] kdj
    [Category] 技术指标
    """
    rsv = (close - llv(low, n)) / (hhv(high, n) - llv(low, n)) * 100
    k = ema(rsv, m1)
    d = ema(k, m2)
    j = 3 * k - 2 * d
    return k, d, j



@decorator
def mp(low, high, period):
    """
    [Definition] period时间周期内的中间价格
    [Category] 技术指标
    median price
    """
    return (ll(low, period) + hh(high, period)) / 2


@decorator
def k(close, low, high, period):
    """
    [Definition] period时间周期内的价格最大值最小值标准化
    [Category] 技术指标
    Stochastic %K
    """
    return (close - ll(low, period)) / (hh(high, period) - ll(low, period))


@decorator
def d(close, low, high, period):
    """
    [Definition] period时间周期内的标准化后的移动平均线
    [Category] 技术指标
    %D is the moving average of %K
    """
    return ma(k(close, low, high, period), period)


@decorator
def r(high, low, close, period):
    """
    [Definition] 在period周期内的威廉指标
    [Category] 技术指标
    Larry William's %R
    """
    return function_wrapper('WILLR', high, low, close, timeperiod=period)


@decorator
def bias(close, period):
    """
    [Definition] period时间周期内价格对平均线的偏差
    [Category] 技术指标
    x-days bias
    """
    return (close - ma(close, period)) / ma(close, period)


@decorator
def oscp(close, period1, period2):
    """
    [Definition] period1时间周期和period2周期内的价格摆动
    [Category] 技术指标
    Price oscillator
    """
    return (ma(close, period1) - ma(close, period2)) / (ma(close, period1))


@decorator
def cci(high, low, close, period):
    """
    [Definition]  Commodity channel index，period时间周期内的价格顺势指标
    [Category] 技术指标
    """
    return function_wrapper('CCI', high, low, close, timeperiod=period)


@decorator
def signalline(close, period1, period2):
    """
    [Definition] period1和period2时间周期内的信号触发线
    [Category] 技术指标
    """
    t1 = ma(close, period1)
    t2 = ma(close, period2)
    return (t1 - t2) / (10 * t2) + t2


@decorator
def mtm(close, period):
    """
    [Definition] Momentum measures change in stock price over last x days
    [Category] 技术指标
    """
    return delta(close, period)


@decorator
def tsi(close, period):
    """
    [Definition] 计算真实力量指数
    [Category] 技术指标
    True strength ixnde
    """
    return 100 * (ema((ema(mtm(close, 1), period)), period)) / (ema((ema(abs(mtm(close, 1)), period)), period))


@decorator
def uo(high, low, close, period1, period2, period3):
    """
    [Definition] 计算终极指标
    [Category] 技术指标
    Ultimate oscillator
    """
    return function_wrapper('ULTOSC', high, low, close, timeperiod1=period1,
                            timeperiod2=period2, timeperiod3=period3)


@decorator
def ma_score(close):
    """
    [Definition] 上穿交叉
    [Category] 技术指标
    短期均线组:由3、5、8、10、12、15移动均线构成，代表短期趋势；
    长期均线组:由30、35、40、45、50、60移动均线构成，代表中长期趋势；
    扩展至更多均线(3日, 4日,...,103日均线)
    $排序 = \frac{\sum_{i=4}^{103}{sign(MA(i-1)-MA(i))}}{100}$
    纯多排序: x> 0, sign(x) = 1; x<=0, sign(x) = 0
    多空排序: x> 0, sign(x) = 1; x<0, sign(x) = -1
    """
    ma_matrix = []
    for i in range(3, 104):
        ma_matrix.append(ma(close, i))
    ma_matrix = np.array(ma_matrix).T
    ma_matrix = np.concatenate((np.nan * np.zeros((close.shape[0], 1)), np.diff(ma_matrix, axis=1)), axis=1)
    score = np.sum(ma_matrix < 0, axis=1) / 100.
    return score


# ==================================== 动作运算符  ====================================
@decorator
def cross(arr1, arr2):
    """
    [Definition] 上穿交叉，arr1上穿arr2返回值为True，否则False
    [Category] 动作
    """
    if type(arr1) is int or type(arr1) is float:
       arr1 = np.ones_like(arr2) * arr1
       res = np.zeros_like(arr2).astype('bool')
    elif type(arr2) is int or type(arr2) is float:
       arr2 = np.ones_like(arr1) * arr2
       res = np.zeros_like(arr1).astype('bool')
    else:
       res = np.zeros_like(arr1).astype('bool')
    cross_c = np.sign(arr1 - arr2)
    res[1:] = np.logical_and(cross_c[1:] == 1, cross_c[:-1] == -1)
    return res



@decorator
def barslast(arr):
    """
    [Definition] 时间序列方向找到上一个值为True位置, find the last True location since now 
    [Category] 动作
    """
    arr = arr == 1
    if arr.dtype != 'bool':
       raise Exception('arr should be bool dtype')
    res = np.zeros_like(arr)*np.nan
    if len(np.where(arr)[0]) ==0:
       return res
    loc = np.where(arr)[0][0]
    for i in xrange(loc,len(arr)):
       if arr[i] == 1:
           res[i] = 0
       else:
           #print i, arr[:i]#, (np.arange(i)[arr[:i]])
           res[i] = i - (np.arange(i)[arr[:i]])[-1]
    return res



@decorator
def ifilter(arr1, arr2, N):
    """
    [Definition] 过滤连续出现的交易信号.
    用法:FILTERX(开仓,平仓,N):N=1,表示仅对开仓信号过滤;
    N=2,表示仅对平仓信号过滤;
    N=0,表示对开仓信号和平仓信号都过滤;
    [Category] 动作
    """ 
    if N==1:
        res = arr1*(arr2 == 0)
        return res
    if N==2:
        res = arr2*(arr1 == 0)
        return res 
    if N==0:
        return (arr1==1) * (arr2==1)


@decorator
def filter(arr, period):
    """
    [Definition]  过滤连续出现的信号.
    用法:FILTER(X,N):X满足条件后，删除其后N周期内的数据置为0.
    例如:FILTER(CLOSE>OPEN,5)查找阳线，5天内再次出现的阳线不被记录在内
    """
    res = np.zeros_like(arr) * np.nan
    for i in xrange(period, len(arr)):
        res[i] = arr[i-period:i]>0