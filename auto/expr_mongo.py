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

def connect_mongodb(db_host, db_port, db_name):
    try:
        client = MongoClient(db_host, db_port)
        db = client[db_name]
    except Exception:
        print('Connect to mongodb error')
    return db



class ExprDB():
    def __init__(self):
        self.mongodb = connect_mongodb(db_host='127.0.0.1', db_port=27017, db_name='AutoResearch')


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



    def write_mongodb(self, pprint=True):
        self._check_values()
        if pprint: 
            print('mongodb write [layer%s] %s' %(self.values.layer, self.values.expr))
        self.mongodb['layer%s' %self.values.layer].insert_one(self.values)



    def update_mongodb(self):
        self._check_values()
        for iterm in self.values.keys():
            self.mongodb['layer%s' %self.values.layer].update_one({'_id': self.values._id}, {"$set": {iterm: self.values[iterm]}})


    def fetch_mongodb(self, db):
        pass



if __name__ == '__main__':
    d = Expr()
    print(d)



