# coding=utf-8
import numpy as np
import pandas as pd
import os

default_names = ["ticker_names", "dates", 'OpenPrice', 'ClosePrice',
				 'HighestPrice', 'LowestPrice', 'Volume','Amount','VWAP', 'TradeStatus', 'Turnover', 'Return']

class PriceVolume():
	def __init__(self, path, data_names=default_names):
		self.path = path
		self.data_names = data_names


	def build(self):
		for i in self.data_names:
			print(os.path.join(self.path, i+'.npy'))
			setattr(self, i, np.load(os.path.join(self.path, i+'.npy')))#.T)


