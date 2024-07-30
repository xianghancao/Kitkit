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

def connect_mongodb(db_nname):
    settings = Munch()
    settings.MONGO_USER = 'admin'
    settings.MONGO_PSW = 'admin123'
    settings.MONGO_HOST = '127.0.0.1'
    settings.MONGO_PORT = '27017'
    client = MongoClient('mongodb://{0}:{1}@{2}:{3}'.format(settings.MONGO_USER,settings.MONGO_PSW,settings.MONGO_HOST,settings.MONGO_PORT))
    db = client[db_nname]
    return db


class ExprDB():
    def __init__(self, pprint=True):
        self.mongodb = connect_mongodb('AutoResearch')
        self.pprint = pprint


    def write_mongodb(self, expr):
        if expr is None: 
            if self.pprint: print('expr is None')
            return
        cursor = self.mongodb['layer%s' %expr['layer']].find_one({'expr':expr['expr']})
        if cursor is None or len(cursor) == 0:
            self.mongodb['layer%s' %expr['layer']].insert_one(expr)
            if self.pprint: print('[ExprDB] mongodb insert layer:%s expr:%s' %(expr['layer'], expr['expr']))
        else:
            if self.pprint: print('Existed! Continue')



    # def update_mongodb(self, expr):
    #     if expr is None:
    #         print('expr is None')
    #         return
    #     for iterm in expr.keys():
    #         if self.pprint:
    #             print('[ExprDB] mongodb insert layer:%s expr:%s' %(expr['layer'], expr['expr']))
    #         self.mongodb['layer%s' %expr['layer']].update_one({'_id': expr['_id']}, {"$set": {iterm: expr[iterm]}})

