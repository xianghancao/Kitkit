# coding=utf-8
import numpy as np
import pandas as pd

class GJ013():    

    def build(self, data) : 
        #ClosePrice = data.ClosePrice    
        #Volume = data.Volume
        #OpenPrice = data.OpenPrice
        high= data.HighestPrice
        low = data.LowestPrice
        vwap = data.VWAP



        alpha = np.sqrt( high*low)-vwap
        print(alpha)

        return alpha


