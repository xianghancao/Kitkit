# coding=utf-8
import numpy as np
import pandas as pd
np.random.RandomState(10)
from munch import Munch
from ...operators import *

class RandomHistoryData():
    def __init__(self, eod, prob=.1, data_range=.1):
        self.config = Munch()
        self.config.prob = prob
        self.config.data_range = data_range
        self.eod = eod


    def gen_ATR_noise(self):
        atr_eod = Munch()
        atr_ = atr(self.eod.ClosePrice, self.eod.HighestPrice, self.eod.LowestPrice, 14)
        loc = np.random.randint(0, len(atr_), int(len(atr_) * self.config.prob))
        # % and max price change % of ATR
        atr_change = atr_ * self.config.data_range * np.array([np.in1d(np.arange(len(atr_)), loc) for i in range(self.eod.ClosePrice.shape[1])]).T
        for i in self.eod.keys():
            
            if i in ['OpenPrice', 'HighestPrice', 'LowestPrice', 'ClosePrice']:
                setattr(atr_eod, i, atr_change + getattr(self.eod, i))
        return atr_eod


    def gen_STD_noise(self):
        std_eod = Munch()
        std = stddev(self.eod.ClosePrice, 20)
        loc = np.random.randint(0, len(std), int(len(std) * self.config.prob))
        # % and max price change % of std
        std_change = std * self.config.data_range * np.array([np.in1d(np.arange(len(std)), loc) for i in range(self.eod.ClosePrice.shape[1])])
        for i in self.eod.keys():
            if i in ['OpenPrice', 'HighestPrice', 'LowestPrice', 'ClosePrice']:
                setattr(std_eod, i, std_change + getattr(self.eod, i))
        return std_eod


    def gen_percent_noise(self):
        per_eod = Munch()
        c = self.eod.ClosePrice
        loc = np.random.randint(0, len(c), int(len(c) * self.config.prob))
        # % and max price change %
        change = c * self.config.data_range * np.array([np.in1d(np.arange(len(c)), loc) for i in range(self.eod.ClosePrice.shap[1])])
        for i in self.eod.keys():
            if i in ['OpenPrice', 'HighestPrice', 'LowestPrice', 'ClosePrice']:
                setattr(per_eod, i, change + getattr(self.eod, i))
        return per_eod





