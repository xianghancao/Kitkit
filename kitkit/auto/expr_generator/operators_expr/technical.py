# coding=utf-8
from .. import prob_engine
pe = prob_engine.ProbEngine()

def delay(x):
    """
    [Definition] 序列x中前period天的价格
    [Category] 技术指标
    delay() value of x d days ago
    """
    return 'delay(%s,%s)' %(x, pe.gen_param('delay', 'period'))



def delta(x):
    """
    [Definition] 间隔period时间的一阶差分
    [Category] 技术指标
    today’s value of x minus the value of x d days ago
    """
    return 'delta(%s,%s)' %(x, pe.gen_param('delta', 'period'))



def delta2(x):
    """
    [Definition] 间隔period时间的二阶差分
    [Category] 技术指标
    x的二阶差分
    """
    return 'delta2(%s,%s,%s)' %(x, pe.gen_param('delta2', 'period1'),
                            pe.gen_param('delta2', 'period2'))


# ====================================Technical====================================


def llv(x):
    """
    [Definition] 数据在n天内的最低价值
    [Category] 技术指标
    """
    return 'llv(%s,%s)' %(x, pe.gen_param('llv', 'period'))



def hhv(x):
    """
    [Definition] 数据在n天内的最高价值
    [Category] 技术指标
    """
    return 'hhv(%s,%s)' %(x, pe.gen_param('hhv', 'period'))




def kama(x):
    
    """
    [Definition] 以period为周期的考夫曼自适应移动平均线
    [Category] 技术指标
    """
    return 'kama(%s,%s)' %(x, pe.gen_param('kama', 'period'))



def midpoint(x):
    """
    [Definition] (highest value-lowest value)/2k
    [Category] 技术指标
    """
    return 'midpoint(%s,%s)' %(x, pe.gen_param('midpoint', 'period'))



def ema(x):
    """
    [Definition] 以period为周期的指数加权移动平均线
    [Category] 技术指标
    """
    return 'ema(%s,%s)' %(x, pe.gen_param('ema', 'period'))



def wma(x):
    """
    [Definition] 以period为周期的加权移动平均线
    [Category] 技术指标
    """
    return 'wma(%s,%s)' %(x, pe.gen_param('wma', 'period'))



def tema(x):
    """
    [Definition] 以period为周期的三指数移动平均线
    [Category] 技术指标
    """
    return 'tema(%s,%s)' %(x, pe.gen_param('tema', 'period'))




def bias(x):
    """
    [Definition] period时间周期内价格对平均线的偏差
    [Category] 技术指标
    x-days bias
    """
    return 'bias(%s,%s)' %(x, pe.gen_param('bias', 'period'))



def oscp(x, period1, period2):
    """
    [Definition] period1时间周期和period2周期内的价格摆动
    [Category] 技术指标
    Price oscillator
    """
    return 'oscp(%s,%s,%s)' %(x, pe.gen_param('oscp', 'period1'),
                            pe.gen_param('oscp', 'period2'))




