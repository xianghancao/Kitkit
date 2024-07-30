# coding=utf-8
import numpy as np
import pandas as pd
from ..operators import *

class a1():    

    def build(self, data) : 
        ClosePrice = data.ClosePrice    
        Volume = data.Volume
        OpenPrice = data.OpenPrice
        five_ma = ma(ClosePrice, 5)   
        ten_ma = ma(ClosePrice, 10)
        #twenty_ma = ma(ClosePrice, 10)
        # MA_5 上穿 MA_10的幅度
        s = sigmoid(Volume)
        #alpha = -twenty_ma/ClosePricePrice
        #alpha = OpenPrice/delay(OpenPrice, 5)
        #alpha = OpenPrice/data.HighestPrice
        return s #np.abs(dif)


