# coding=utf-8
import expr_generator
prob_engine = expr_generator.ExprGenerator()



# ====================================元素级====================================
def abs(x):
    """
    [Definition] 对x取绝对值
    [Category] 元素级
    """
    return 'abs(%s)' %x



def sqrt(x):
    """
    [Definition] 对x开方
    [Category] 元素级
    """
    # if ~np.array((x >= 0)).all():
    #   raise OpException('NANs exist in function sqrt()!')
    return 'sqrt(%s)' %x



def square(x):
    """
    [Definition] 对x平方
    [Category] 元素级
    """
    return 'square(%s)' %x



def exp(x):
    """
    [Definition] 对x做指数运算
    [Category] 元素级
    """
    return 'exp(%s)' %x



def log(x):
    """
    [Definition] 对x做对数运算
    [Category] 元素级
    """

    # if ~np.array((x > 0)).all():

    # raise OpException('NANs exist in function log()!')
    return 'log(%s)' %x



def log10(x):
    """
    [Definition] 对x做以10为低的对数运算
    [Category] 元素级
    """
    # if ~np.array((x > 0)).all():
    #   raise OpException('NANs exist in function log10()!')
    return 'log10(%s)' %x



def log2(x):
    """
    [Definition] 对x做以2为低的对数运算
    [Category] 元素级
    """
    # if ~np.array((x > 0)).all():
    #   raise OpException('NANs exist in function log2()!')
    return 'log2(%s)' %x



def sign(x):
    """
    [Definition] x<0 返回-1；x>0 返回1； x==0 返回0
    [Category] 元素级
    """
    return 'sign(%s)' %x



def signedpower(x):
    """
    [Definition] 对x的绝对值做pow次方，并保存x的符号
    [Category] 元素级
    带符号的power
    """
    return 'signedpower(%s,%s)' %(x, prob_engine.gen_param('signedpower', 'pow'))



def sigmoid(x):
    """
    [Definition] 序列x的S型生长曲线
    [Category] 特殊符号函数
    """
    return 'sigmoid(%s)' %x



def nike(x):
    """
    [Definition] 序列x的对勾函数
    [Category] 特殊符号函数
    """
    return 'nike(%s)' %x
