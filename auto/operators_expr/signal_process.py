# coding=utf-8
import expr_generator
prob_engine = expr_generator.ExprGenerator()


def decay_linear(x):
    """
    [Definition] 序列x的前period日权重滑动平均线(WMA)，较近日期权重较高，较远日期千重较低, weighted moving average over the past d days with linearly decaying  weights d, d – 1, …, 1 (rescaled to sum up to 1)
    [Category] 信号处理
    """
    return 'decay_linear(%s,%s)' %(x, prob_engine.gen_param('decay_linear', 'period'))



def decay_exponent(x):
    """
    [Definition] 序列x的前period日指数滑动平均线(EMA), exponential moving average over the past d days with exponent decaying  weights d, d – 1, …, 1 (rescaled to sum up to 1)
    [Category] 信号处理
    """
    return 'decay_exponent(%s,%s)' %(x, prob_engine.gen_param('decay_exponent', 'period'))


def decay_fibonacci(x):
    """
    [Definition] 序列x的前period日权重滑动滚动加权平均线，加权系数为菲波那切数列, rolling fibonacci-number weighted
    [Category] 信号处理
    """
    return 'decay_fibonacci(%s,%s)' %(x, prob_engine.gen_param('decay_fibonacci', 'period'))

