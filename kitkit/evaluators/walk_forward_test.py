# encoding: utf-8
import os, sys
fpath = os.path.dirname(os.path.realpath(__file__))
ROOT_PATH = os.path.split(fpath)[0]
sys.path.append(ROOT_PATH)
sys.path.append(os.path.join(ROOT_PATH, 'utils'))
sys.path.append(os.path.join(ROOT_PATH, 'lib'))
from factor_pool_connect import FactorPoolConnect
import backtest
from munch import Munch
import numpy as np 
import pandas as pd 


########################################################################
class WalkForward(object):
    """
    walk forward method
      -------------------------------------------------------
      |     train period 1              | predict period 1  | 
      -------------------------------------------------------
                            ----------------------------------------------------
                            |     train period 2            |  predict period 2 |
                            ----------------------------------------------------
                                                    -------------------------------------------------
                                                    |     train period 3        |  predict period 3 |
                                                    -------------------------------------------------
    """
    def __init__(self, policy_path, start=None, end=None, lookback_bars=0, train_bars=120, predict_bars=20):
        print 'WF apply for %s' %policy_path
        self.config = Munch()
        self.config.policy_path = policy_path
        self.config.start = start
        self.config.end = end
        self.config.train_bars = train_bars
        self.config.predict_bars = predict_bars
        self.config.lookback_bars = lookback_bars


    #----------------------------------------------------------------------
    def run(self):
        self._load_factor()
        self._set_walk_dates()
        self._set_walk_step()
        self.walk_forward()
        self.plot()
        self.dump()

        
    #----------------------------------------------------------------------
    def _load_factor(self):
        f = FactorPoolConnect(path='/share/FactorPoolRaw2/', all_sample=True)
        self.all_factor_dict = f.load_factor('resample_wgts', 'resample_return')


    #----------------------------------------------------------------------
    def _set_walk_dates(self):
        self.config.all_dates = self.all_factor_dict.A1711290431_1day.resample_wgts.index.values
        self.WF_dates_start_idx, self.WF_dates_end_idx = 0, len(self.config.all_dates)
        if self.config.start is not None:
            self.WF_dates_start_idx = np.where(pd.to_datetime(self.config.all_dates)>=pd.to_datetime(self.config.start))[0][0]
        if self.config.end is not None:
            self.WF_dates_end_idx = np.where(pd.to_datetime(self.config.all_dates)<pd.to_datetime(self.config.end))[0][0]


    #----------------------------------------------------------------------
    def _set_walk_step(self):
        self.config.WF_dates, self.config.WF_dates_idx = {}, {}
        walk_count = 1
        for i in xrange(self.WF_dates_start_idx + self.config.lookback_bars + self.config.train_bars + self.config.predict_bars,
                      self.WF_dates_end_idx,
                      self.config.predict_bars):
            self.config.WF_dates_idx[walk_count] = {'train_start': i-self.config.predict_bars-self.config.train_bars,
                                         'train_end':i-self.config.predict_bars,
                                         'predict_start':i-self.config.predict_bars,
                                         'predict_end':i}
            self.config.WF_dates[walk_count] = {'train_start': self.config.all_dates[self.config.WF_dates_idx[walk_count]['train_start']],
                                         'train_end':self.config.all_dates[self.config.WF_dates_idx[walk_count]['train_end']],
                                         'predict_start':self.config.all_dates[self.config.WF_dates_idx[walk_count]['predict_start']],
                                         'predict_end':self.config.all_dates[self.config.WF_dates_idx[walk_count]['predict_end']]}
            walk_count += 1
        from prettytable import PrettyTable
        x = PrettyTable(['walk #', 'train_start - train_end', 'predict_start - predict_end'])
        for i in self.config.WF_dates:
            x.add_row([i, '%s - %s' %(self.config.WF_dates[i]['train_start'], self.config.WF_dates[i]['train_end']), '%s - %s' %(self.config.WF_dates[i]['predict_start'], self.config.WF_dates[i]['predict_end'])])
        print x


    #----------------------------------------------------------------------
    def one_walk_forward(self, policy_name, is_factor_dict, oos_factor_dict, i):
        import imp
        m = imp.load_source('policy', policy_name)
        policy = m.Policy()
        # train
        is_factor = policy.train(is_factor_dict)
     
        # predict
        oos_factor = policy.predict(oos_factor_dict)
        return Munch({i:Munch({'oos_factor': oos_factor, 'is_factor':is_factor})})


    #----------------------------------------------------------------------
    def walk_forward(self):
        self.policy_record = Munch()
        self.is_resample_return, self.is_resample_dates, self.oos_resample_return, self.oos_resample_dates = {}, {}, {}, {} 
        for i in np.sort(self.config.WF_dates.keys()):
            is_start = self.config.WF_dates[i]['train_start']
            is_end = self.config.WF_dates[i]['train_end']
            oos_start = self.config.WF_dates[i]['predict_start']
            oos_end = self.config.WF_dates[i]['predict_end']

            is_index = np.logical_and(pd.to_datetime(self.config.all_dates)>=pd.to_datetime(is_start),
                                 pd.to_datetime(self.config.all_dates)<pd.to_datetime(is_end))
            oos_index = np.logical_and(pd.to_datetime(self.config.all_dates)>=pd.to_datetime(oos_start),
                                 pd.to_datetime(self.config.all_dates)<pd.to_datetime(oos_end))

            is_factor_dict, oos_factor_dict = Munch(), Munch()
            for j in self.all_factor_dict:
                is_factor_dict[j], oos_factor_dict[j] = Munch(), Munch()
                for k in self.all_factor_dict[j]:
                    is_factor_dict[j][k] = self.all_factor_dict[j][k][is_index]
                    oos_factor_dict[j][k] = self.all_factor_dict[j][k][oos_index]
            self.is_resample_return[i] = is_factor_dict[j].resample_return.values
            self.is_resample_dates[i] =  is_factor_dict[j].resample_return.index.values
            self.oos_resample_return[i] = oos_factor_dict[j].resample_return.values
            self.oos_resample_dates[i] =  oos_factor_dict[j].resample_return.index.values
            print 'WF #%s' %i
            self.policy_record.update(self.one_walk_forward(self.config.policy_path, is_factor_dict.copy(), oos_factor_dict.copy(), i))


    #----------------------------------------------------------------------
    def plot(self):
        print u'WF组合收益图'
        self.all_sample_factor = np.vstack([self.policy_record[1].is_factor, self.policy_record[1].oos_factor])
        returns = np.vstack([self.is_resample_return[1], self.oos_resample_return[1]])
        dates = np.append(self.is_resample_dates[1], self.oos_resample_dates[1])
        is_oos_arr = np.append(np.zeros_like(self.policy_record[1].is_factor), np.ones_like(self.policy_record[1].oos_factor))
        for i in np.sort(self.config.WF_dates.keys())[1:]:
            self.all_sample_factor = np.vstack([self.all_sample_factor, self.policy_record[i].oos_factor])
            returns = np.vstack([returns, self.oos_resample_return[i]])
            dates = np.append(dates, self.oos_resample_dates[i])
            is_oos_arr = np.append(is_oos_arr, i * np.ones_like(self.policy_record[i].oos_factor))

        #print factor.shape, returns.shape, dates.shape
        #print is_oos_arr.shape
        #print factor
        bt = backtest.BackTest(self.all_sample_factor, returns, dates)
        bt.run()
        bt.stats_info()
        bt.two_in_one()
        bt.ts_plot()
         #is_oos_arr=is_oos_arr,
                      #title='WF train:%s predict:%s' %(self.config.train_bars, self.config.predict_bars))
                      #output='/home/dev/FalconPolicy/WalkForward/' + self.config.policy_path.split('/')[-1].split('.py')[0] + '_WF_train_%s_predict_%s.png' %(self.config.train_bars, self.config.predict_bars))

        print u'样本外收益图'
        self.oos_sample_factor = self.policy_record[1].oos_factor
        returns = self.oos_resample_return[1]
        dates = self.oos_resample_dates[1]
        is_oos_arr = np.ones_like(self.policy_record[1].oos_factor)
        for i in np.sort(self.config.WF_dates.keys())[1:]:
            self.oos_sample_factor = np.vstack([self.oos_sample_factor, self.policy_record[i].oos_factor])
            returns = np.vstack([returns, self.oos_resample_return[i]])
            dates = np.append(dates, self.oos_resample_dates[i])
            is_oos_arr = np.append(is_oos_arr, i * np.ones_like(self.policy_record[1].oos_factor))

        bt = backtest.BackTest(self.oos_sample_factor, returns, dates)
        bt.run()
        bt.stats_info()
        bt.two_in_one()
        bt.ts_plot()

    #----------------------------------------------------------------------
    def dump(self):
        pass
        # # 保存结果
        # factor = self.policy_record[1].oos_factor.resample_wgts
        # returns = self.policy_record[1].oos_factor.resample_return
        # dates = self.policy_record[1].oos_factor.resample_dates
        # for i in np.sort(self.config.WF_dates.keys())[1:]:
        #     factor = np.vstack([factor, self.policy_record[i].oos_factor.resample_wgts])
        #     returns = np.vstack([returns, self.policy_record[i].oos_factor.resample_return])
        #     dates = np.append(dates, self.policy_record[i].oos_factor.resample_dates)

        # bt = backtest.BackTest(factor, returns, dates)
        # bt.run()
        # bt.stats_df.to_csv('/home/dev/FalconPolicy/WalkForward/' + self.config.policy_path.split('/')[-1].split('.py')[0] + '_WF_train_%s_predict_%s_oos.csv' %(self.config.train_bars, self.config.predict_bars))






 