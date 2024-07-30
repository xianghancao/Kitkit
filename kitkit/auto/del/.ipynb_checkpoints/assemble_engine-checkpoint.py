# coding=utf-8
# 20170426
import numpy as np
import pandas as pd
from munch import Munch
import operators_expr 
import inspect
import json, os
from prob_engine import ProbEngine
from data_structure import DataStructure
from pymongo import MongoClient
import uuid
from tqdm import tqdm

"""
功能：
- 将元素和运算符组合，并返回
- 将两个运算符组合，并返回
- 查重
"""

def connect_mongodb(db_host, db_port, db_name):
    try:
        client = MongoClient(db_host, db_port)
        db = client[db_name]
    except Exception, e:
        print e, 'Connect to mongodb error'
    return db





class AssembleEngine():
    def __init__(self):
        self.prob_engine = ProbEngine()
        self.mongodb = connect_mongodb(db_host='127.0.0.1', db_port=27017, db_name='Machine')


    def assemble_expr(self, layer_num):
        """
        递归
        """
        layer_num = int(layer_num)
        if layer_num == 0:
            return self.prob_engine.get_one_element()
        else:
            while True:
                #print 'layer%s' %layer_num
                op = self.prob_engine.get_one_operator()
                args_list = []
                op_arg = inspect.getargspec(getattr(operators_expr, op))
                for i in range(len(op_arg.args)):
                    args_list.append(self.assemble_expr(layer_num-1))
                layer_num -= 1
                return getattr(operators_expr, op)(*args_list)



    def gen_layer0(self):
        for i in ['OpenPrice', 'HighestPrice', 'LowestPrice', 'ClosePrice', "Volume", "Position", "VWAP", "Return", "TurnOver"]:
            expr_object = DataStructure()
            #expr_object.values.id = str(uuid.uuid1())
            expr_object.values.expr = str(i)
            expr_object.values.type = 'elements'
            expr_object.values.layer = 0
            expr_object.write_mongodb(self.mongodb)


    def gen_layerN(self, layer, num=10):
        if not isinstance(layer, int): raise Exception('layer should be int type!')
        layer = int(layer)
        for i in tqdm(xrange(num), desc='layer%s generate expr' %layer):
            expr_object = DataStructure()
            expr_object.values.expr = str(i)
            expr_object.values.type = 'operators'
            expr_object.values.layer = layer
            expr_object.values.expr = self.assemble_expr(layer)
            expr_object.write_mongodb(self.mongodb)

















