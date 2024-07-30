# coding=utf-8
import numpy as np
import pandas as pd
import os


class Universe():
    def __init__(self, path):
        self.path = path

        
    def build(self):
        print('[Data][universe]' + self.path)
        df = pd.read_excel(self.path)
        return df['成分券代码Constituent Code'].values