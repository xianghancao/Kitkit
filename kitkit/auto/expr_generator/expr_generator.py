
# coding=utf-8
# 20180425
import numpy as np
import pandas as pd
import os
import inspect
from datetime import datetime
import yaml
from . import operators_expr
from .prob_engine import ProbEngine



class ExprGenerator(ProbEngine):
    def __init__(self, pprint=True):
        super().__init__()
        self._init_operators_blacklist()
        self.pprint = pprint

    # --------------------------------------------------------------------
    def _init_operators_blacklist(self):
        yaml_path = os.path.join(os.path.dirname(__file__),'operators_blacklist.yaml')
        with open(yaml_path, 'r') as ff:
            self.operators_blacklist = yaml.load(ff) 



    # --------------------------------------------------------------------
    def _get_one_expr_str(self, layer_num):
        layer_num = int(layer_num)
        if layer_num == 0:
            return self.get_one_element()
        else:
            while True:
                #print('layer:%s' %layer_num)
                op = self.get_one_operator()
                args_list = []
                op_arg = inspect.getargspec(getattr(operators_expr, op))
                for i in range(len(op_arg.args)):
                    args_list.append(self._get_one_expr_str(layer_num-1))
                layer_num -= 1
                return getattr(operators_expr, op)(*args_list)

    # --------------------------------------------------------------------
    def _expr_blacklist_check(self, expr_str):
        for i in self.operators_blacklist['blacklist']:
            if i in expr_str:
                if self.pprint: print('[ExprGenerator] Blacklist rules blocked this expr_str: %s' %(expr_str))
                return None
        return expr_str

   # --------------------------------------------------------------------
    def get_one_expr(self, layer_num):
        expr_str = self._get_one_expr_str(layer_num)
        if self._expr_blacklist_check(expr_str) is None: return None
        expr = {
            "expr": expr_str,
            "layer": layer_num,
            "create_date": str(datetime.now())[:19],
            "backtest": "Undo"
        }
        if self.pprint: print('[ExprGenerator] layer:%s expr:%s' %(expr['layer'], expr['expr']))
        return expr





