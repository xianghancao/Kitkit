# coding=utf-8


#====================================逻辑====================================

def iff(cond, expr1, expr2):
    '''
    [Definition] 如果cond成立，则为expr1，否则为expr2，cond? expr1: expr2，cond is a matrix with True or False in each postion
    [Category] 逻辑
    '''
    return 'iff(%s,%s,%s)' %(cond, expr1, expr2)


    

def or_expr(expr1, expr2):
    """
    [Definition] expr1和expr2逻辑运算
    [Category] 逻辑

    """
    return 'or_expr(%s,%s)' %(expr1, expr2)



def max(x, y):
    """
    [Definition] x和y对应位置元素比大小，取最大值
    [Category] 逻辑
    """
    return 'max(%s,%s)' %(x,y)



def min(x, y):
    """
    [Definition] x和y对应位置元素比大小，取最小值
    [Category] 逻辑
    """
    return 'min(%s,%s)' %(x,y)

