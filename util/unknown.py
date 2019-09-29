def Rsquared(y):
    # return R^2 where x and y are array-like
    from scipy.stats import linregress
    x = np.arange(len(y))
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    return r_value**2, x*slope + intercept


def scale_one(x):
    #归一化处理
    x[np.isinf(x)] = np.nan
    res = (x.T / (np.nansum(np.abs(x), axis=1) + 1e-20)).T
    return res


def equal_wgts(x):
    x = np.nan_to_num(x)
    x[x > 0] = 1
    x[x < 0] = -1
    return x