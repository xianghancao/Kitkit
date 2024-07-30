# coding=utf-8
# 20170426
import numpy as np
import pandas as pd
from munch import Munch
import json, os
from pymongo import MongoClient
from datetime import datetime

"""
功能：
- 套入模版
- 写入数据，json格式到指定路径下
- 读取数据，json格式
- 查找指定字段
- 替换指定字段
"""
class DataStructure():
    def __init__(self):
        self.values = Munch({
            "expr": None,
            "dtype": None, 
            "priority": None,
            "layer": None,
            "error": None,
            "IS_backtest": "Undo",
            "OOS_backtest": "Undo",
            "author": "dev",
            "create_date": str(datetime.now())[:19]
        })


    def __str__(self):
        return str(pd.DataFrame(self.values, index=['']))


    def _load_json(self, path):
        with open(path, 'r') as ff:
            self.values = Munch(json.load(ff))



    def _write_json(self, path, expr_dict):
        #if not os.path.exists(path): raise Exception('path %s not exists!' %path)
        with open(path, 'w') as ff:
            print >> ff, json.dumps(expr_dict)


    def _check_values(self):
        if self.values.expr == 'None':
            raise Exception('expr is None')
        if self.values.layer == 'None':
            raise Exception('layer is None, should be 1, 2, 3...')


    # def read(self, layer, id_):
    #   self._load_json(os.path.join('/home/dev/Machine/output', layer, id_+'.json'))


    def write_mongodb(self, db):
        self._check_values()
        print '[layer%s] %s write to mongo' %(self.values.layer, self.values.expr)
        db['layer%s' %self.values.layer].insert_one(self.values)



    def update_mongodb(self, db):
        self._check_values()
        for iterm in self.values.keys():
            db['layer%s' %self.values.layer].update_one({'_id': ObjectId(self.values.id)}, {"$set": {iterm: self.values[iterm]}})


    def fetch_mongodb(self, db):
        pass



if __name__ == '__main__':
    d = DataStructure()
    d.values.id = 'test'
    d.values.expr = 'test'
    d.values.layer = 0
    mongo_db = MongoClient(host='127.0.0.1', port=27017)
    d.write_mongodb(mongo_db.Machine)




