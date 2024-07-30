# coding=utf-8


# ====================================三角函数====================================

def sin(x):
    """
    [Definition] x的正弦函数
    [Category] 三角函数
    """
    return 'sin(%s)' %x



def cos(x):
    """
    [Definition] x的余弦函数
    [Category] 三角函数
    """
    return 'cos(%s)' %x



def tan(x):
    """
    [Definition] x的正切函数
    [Category] 三角函数
    Notes:np.nan seems not to check domain of definition!
    """
    return 'tan(%s)' %x


# ====================================反三角函数====================================



def arcsin(x):
    """
    [Definition] x的反正弦函数
    [Category] 反三角函数
    """
    # if ~(np.array(np.abs(x) <= 1)).all():
    #   raise OpException('NANs exist in function arcsin()!')
    return 'arcsin(%s)' %x



def arccos(x):
    """
    [Definition] x的反余弦函数
    [Category] 反三角函数
    """
    # if ~(np.array(np.abs(x) <= 1)).all():
    #   raise OpException('NANs exist in functoin arccos()!')
    return 'arccos(%s)' %x


def arctan(x):
    """
    [Definition] x的反正切函数
    [Category] 反三角函数
    """
    return 'arctan(%s)' %x

# ====================================双曲函数====================================



def sinh(x):
    """
    [Definition] x的双曲正弦函数
    [Category] 双曲函数
    sinh = (e^x - e^-x) / 2
    """
    return 'sinh(%s)' %x


def cosh(x):
    """
    [Definition] x的双曲余弦函数
    [Category] 双曲函数
    cosh = (e^x + e^-x) / 2
    """
    return 'cosh(%s)' %x


def tanh(x):
    """
    [Definition] x的双曲正切函数
    [Category] 双曲函数
    tanh = (e^x - e^-x) / (e^x + e^-x)
    """
    return 'tanh(%s)' %x

# ====================================反双曲函数====================================



def arcsinh(x):
    """
    [Definition] x的反双曲正弦函数
    [Category] 反双曲函数
    domain of definition: R
    """
    return 'arcsinh(%s)' %x


def arccosh(x):
    """
    [Definition] x的反双曲余弦函数
    [Category] 反双曲函数
    domain of definition: [1, +Inf]
    """
    # if ~(np.array(x >= 1)).all():
    #   raise OpException('Warning: NANs exist in function arccosh()!')
    return 'arccosh(%s)' %x


def arctanh(x):
    """
    [Definition] x的反双曲正切函数
    [Category] 反双曲函数
    domain of definition: (-1, 1)
    """
    return 'arctanh(%s)' %x