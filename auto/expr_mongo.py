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



    def write_mongodb(self, expr):
        if expr is None: 
            print('expr is None')
            return

        cursor = self.mongodb['layer%s' %expr['layer']].find_one({'expr':expr['expr']})
        if cursor is None or len(cursor) == 0:
            self.mongodb['layer%s' %expr['layer']].insert_one(expr)
            print('[ExprDB] mongodb insert layer:%s expr:%s' %(expr['layer'], expr['expr']))
        else:
            print('Existed! Continue')



    def update_mongodb(self, expr):
        if expr is None:
            print('expr is None')
            return
        for iterm in expr.keys():
            print('[ExprDB] mongodb insert layer:%s expr:%s' %(expr['layer'], expr['expr']))
            self.mongodb['layer%s' %expr['layer']].update_one({'_id': expr['_id']}, {"$set": {iterm: expr[iterm]}})

