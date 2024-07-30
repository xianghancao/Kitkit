# coding=utf-8
from .. import prob_engine
pe = prob_engine.ProbEngine()


def ts_sum(x):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求和
    [Category] 统计
    """
    return 'ts_sum(%s,%s)' %(x, pe.gen_param('ts_sum','period'))




def ts_product(x):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动平方加和
    [Category] 统计
    time-series product over the past period days
    """
    return 'ts_product(%s,%s)' %(x, pe.gen_param('ts_product','period'))



def ts_min(x):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求最小值
    [Category] 统计
    """
    # 取前n天数据的最小值
    return 'ts_min(%s,%s)' %(x, pe.gen_param('ts_min','period'))



def ts_max(x):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求最大值
    [Category] 统计
    """
    return 'ts_max(%s,%s)' %(x, pe.gen_param('ts_max','period'))



def ts_argmax(x):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求最大值的位置，过去period天的最大值的位置，范围[1,period]
    [Category] 统计
    """
    return 'ts_argmax(%s,%s)' %(x, pe.gen_param('ts_argmax','period'))



def ts_argmin(x):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求最小值的位置，过去period天的最小值的位置，范围[1,period]
    [Category] 统计

    """
    return 'ts_argmin(%s,%s)' %(x, pe.gen_param('ts_argmin','period'))



def rank(x):
    """
    [Definition] 对x进行空头和多头的横截面排序, 
    [Category] 统计
    这里需要注意，不能分别对多头和空头进行排序，不然会出现不对称性
    """
    return 'rank(%s)' %x

    

def ts_rank(x):
    """
    [Definition] 对x中的每个时间序列在period范围内进行滚动排序
    [Category] 统计
    st.mstats.rankdata算法太慢, 用np.argsort替代，需要改进
    """
    return 'ts_rank(%s,%s)' %(x, pe.gen_param('ts_rank','period'))



def ma(x):
    """
    [Definition] 对x中的每个时间序列在period范围内滚动求均值
    [Category] 统计
    """
    return 'ma(%s,%s)' %(x, pe.gen_param('ma','period'))




def skewness(x):
    """
    [Definition] 序列x的前period日偏度值
    [Category] 统计
    """
    return 'skewness(%s,%s)' %(x, pe.gen_param('skewness','period'))



def kurtosis(x):
    """
    [Definition] 序列x的前period日峰度值
    [Category] 统计
    return the rolling kurtosis of x
    nan_policy: decide how to handle when input contains nan.
                'omit' performs the calculations ignoring nan values.
                Default is 'propagate' that will let kurtosis return nan
    for details:http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kurtosis.html
    """
    return 'kurtosis(%s,%s)' %(x, pe.gen_param('kurtosis','period'))



def k_moment(x):  
    """
    [Definition] 序列x前period日的滚动k阶中心距
    [Category] 统计
    计算x的滚动k阶中心距
    """
    return 'k_moment(%s,%s,%s)' %(x, pe.gen_param('k_moment','period'),
                                    pe.gen_param('k_moment', 'pow'))



def geometric_mean(x):
    """
    [Definition] 序列x的滚动几何平均数, [sqrt(x1*x2), sqrt(x2*x3), …… , sqrt(xn-1*xn)], Notes:the first element is nan
    [Category] 特殊符号函数
    """
    return 'geometric_mean(%s)' %x



def beta(high, low):
    """
    [Definition] CAPM模型中的beta系数
    [Category] 统计
    """
    return 'beta(%s,%s,%s)' %(high, low, pe.gen_param('beta', 'period'))



def linearreg(x):
    """
    [Definition] 线性回归
    [Category] 统计
    """
    return 'linearreg(%s,%s)' %(x, pe.gen_param('linearreg', 'period'))



def linearreg_angle(x):
    """
    [Definition] 线性回归的一种最小角回归，主要针对解决高维回归问题
    [Category] 统计
    """
    return 'linearreg_angle(%s,%s)' %(x, pe.gen_param('linearreg_angle', 'period'))



def linearreg_intercept(x):
    """
    [Definition] 回归的截距
    [Category] 统计
    """
    return 'linearreg_intercept(%s,%s)' %(x, pe.gen_param('linearreg_intercept', 'period'))



def linearreg_slope(x):
    """
    [Definition] 线性回归的斜率
    [Category] 统计
    """
    return 'linearreg_slope(%s,%s)' %(x, pe.gen_param('linearreg_slope', 'period'))



def tsf(x):
    """
    [Definition] 时间序列预测
    [Category] 统计
    """
    return 'linearreg_slope(%s,%s)' %(x, pe.gen_param('linearreg_slope', 'period'))



def stddev(x):  # 标准差
    """
    [Definition] 序列x在前period日的标准差
    [Category] 统计
    """
    return 'stddev(%s,%s)' %(x, pe.gen_param('stddev', 'period'))



def var(x):
    """  
    [Definition] 序列x在前period日的方差
    [Category] 统计
    """
    return 'var(%s,%s)' %(x, pe.gen_param('var', 'period'))



def scale(x):  # 缩放运算
    """
    [Definition] 序列x的归一化，数据在（-1,1）之间
    [Category] 统计
    rescaled x such that sum(abs(x)) = a (the default is a = 1)
    """
    return 'scale(%s)' %x



def correlation(x, y):
    """
    [Definition] 序列x和y在前period日的皮尔逊相关系数
    [Category] 统计
    """
    return 'correlation(%s,%s,%s)' %(x, y, pe.gen_param('correlation', 'period'))



def covariance(x, y):
    """
    [Definition] 序列x和y在前period日的协方差,使用皮尔森相关系数的公式算协方差公式
    [Category] 统计
    """
    return 'covariance(%s,%s,%s)' %(x, y, pe.gen_param('covariance', 'period'))



def count_nans(x):
    """
    [Definition] 最近period周期内序列x中NAN元素的个数
    [Category] 统计

    return the number of NANs in x during last period
    """
    return 'count_nans(%s,%s)' %(x, pe.gen_param('count_nans', 'period'))

    


def ts_count(cond):
    """
    [Definition] 最近period周期内序列x中满足cond的元素个数
    [Category] 统计
    return the number of cond=True in x during last period
    """
    return 'ts_count(%s,%s)' %(cond, pe.gen_param('ts_count', 'period'))


