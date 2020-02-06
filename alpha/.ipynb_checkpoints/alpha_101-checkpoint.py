# coding=utf-8
import numpy as np
import pandas as pd
import operators

class Alpha_101():    

    def build(self, data) : 
        ClosePrice = data.ClosePrice    
        Volume = data.Volume
        OpenPrice = data.OpenPrice
        five_ma = operators.ma(ClosePrice, 5)   
        ten_ma = operators.ma(ClosePrice, 10)
        #twenty_ma = operators.ma(ClosePrice, 10)
        # MA_5 上穿 MA_10的幅度
        dif = (five_ma-ten_ma)/ten_ma  
        #alpha = -twenty_ma/ClosePricePrice
        #alpha = OpenPrice/delay(OpenPrice, 5)
        #alpha = OpenPrice/data.HighestPrice
        return dif


