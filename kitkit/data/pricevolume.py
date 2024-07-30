# coding=utf-8
import numpy as np
import pandas as pd
import os

default_names = ["ticker_names", "dates", 'OpenPrice', 'ClosePrice',
				 'HighestPrice', 'LowestPrice', 'Volume','VWAP', 'TradeStatus', 'Return', 'VolChg']

class PriceVolume():
	def __init__(self, path, data_names=default_names):
		self.path = path
		self.data_names = data_names

        
	def build(self):
		print('[Data][pricevolume]' + self.path)
		for i in self.data_names:
			arr = np.load(os.path.join(self.path, i+'.npy'))
			if len(arr.shape)>1 and arr.shape[0]<=arr.shape[1]:
				raise Exception('pls check %s dates number should above stock number!' %i)
			setattr(self, i, arr)
		print('[Data][pricevolume] start:%s end:%s' %(self.dates[0], self.dates[-1]))
            

            
            


