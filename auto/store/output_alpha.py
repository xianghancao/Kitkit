# coding=utf-8
# 20180426
import numpy as np
import pandas as pd
from munch import Munch
import json, os, sys
from prob_engine import ProbEngine
from data_structure import DataStructure
sys.path.append('/home/dev/')
from FalconAlpha.simlib.process.backtest import BackTest
from FalconAlpha.operators import *
from tqdm import tqdm
from datetime import datetime
import pymongo
from pymongo import MongoClient
import time
from alpha_cal import AlphaCal

def gen_signal_output(ac, alpha_ds, count):
    signal_name = 'S' + str(alpha_ds.values._id)
    output_dir = os.path.join('/home/dev/Machine/output2/', signal_name)  
    
    if not os.path.exists(output_dir): os.mkdir(output_dir)            
    ac.cal_one_alpha(alpha_ds, output_dir=output_dir)
    print count


class OutputAlphas():
    def __init__(self, db_host, db_port, db_name):
        self.config = Munch()
        self.config.db_host = db_host
        self.config.db_port = db_port
        self.config.db_name = db_name


        self.config.queue_host = db_host
        self.config.queue_port = 5000
        #self.config.queue_authkey = 'abc'
        self.config.launch_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.config.pid = os.getpid()
        print self.config



    def connect_mongodb(self):
        try:
            client = MongoClient(self.config.db_host, self.config.db_port)
            db = client[self.config.db_name]
        except Exception, e:
            print e, 'Connect to mongodb error'
        return db


    def fetch_data(self, col, data_num):
        # 提取数据，优先级降序排列
        print 'fetch_data (num:%s)...' %data_num
        return col.find({}).sort([("IS_alpha_sharpe", pymongo.DESCENDING), \
                               ('OOS1_alpha_sharpe', pymongo.DESCENDING)]).limit(data_num) 



    def gen_signal_file(self, alpha_ds):
        signal_name = 'S' + str(alpha_ds.values._id)
        output_dir = os.path.join('/home/dev/Machine/output/', signal_name)        
        if not os.path.exists(output_dir): os.mkdir(output_dir)
        with open('/home/dev/Machine/signal_template/signal_template.yaml', 'r') as f:
            with open(os.path.join(output_dir, signal_name+'.yaml'), 'w') as p:
                line = []
                for i in f:
                    i = i.replace('signal_template', signal_name)
                    i = i.replace('/n', '')
                    print >> p, i

        with open('/home/dev/Machine/signal_template/signal_template.py', 'r') as f:
            with open(os.path.join(output_dir, signal_name+'.py'), 'w') as p:
                line = []
                for i in f:
                    i = i.replace('signal_template', signal_name)
                    i = i.replace('/n', '')
                    i = i.replace('need_replace', alpha_ds.values.expr)
                    print >> p, i






    def run(self):
        self.db = self.connect_mongodb()
        cursor = self.fetch_data(self.db['warehouse2'], 17000)
        self.ac = AlphaCal(sampling='ALL')
        path = '/home/dev/Machine/output2/'
        list_signal = os.listdir(path)
        from multiprocessing import Pool
        p = Pool(50)
        p.daemon = True
        count = 0
        for i in tqdm(cursor):
            ds = DataStructure(i)
            if 'S%s' %ds.values._id in list_signal:
                continue
            #gen_signal_output(self.ac, DataStructure(i))
            count += 1
            p.apply_async(gen_signal_output, (self.ac, DataStructure(i), '%s/%s' %(count, cursor.count()),, ))
        p.close()
        p.join()
            #raise Exception()





if __name__ == '__main__':
    fa = OutputAlphas(db_host='127.0.0.1', db_port=27017, db_name='Machine')
    fa.run()