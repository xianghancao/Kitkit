# encoding: utf-8
from ..backtest import backtest
from ..method.merge import Merge
import numpy as np
import pandas as pd 
from munch import Munch
import matplotlib
matplotlib.use('Agg')
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import talib
import time
from tqdm import tqdm
color_list = ['steelblue', 'orangered', 'forestgreen']




class GridFigure(object):
    """
    It makes life easier with grid plots
    """

    def __init__(self, rows, cols, sub_figsize=(15, 2.5)):

        self.rows = rows
        self.cols = cols
        self.fig = plt.figure(figsize=(sub_figsize[0], rows*sub_figsize[1]))
        self.gs = gridspec.GridSpec(rows, cols, wspace=0.4, hspace=0.3)
        self.curr_row = 0
        self.curr_col = 0

    def next_row(self):
        if self.curr_col != 0:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, :])
        self.curr_row += 1
        return subplt

    def next_cell(self):
        if self.curr_col >= self.cols:
            self.curr_row += 1
            self.curr_col = 0
        subplt = plt.subplot(self.gs[self.curr_row, self.curr_col])
        self.curr_col += 1
        return subplt

    def show(self):
        plt.show(self.fig)
        
    def close(self):
        plt.close(self.fig)
        self.fig = None
        self.gs = None


def combination_2(arr):
    # C(3,2)
    m = len(arr)
    res = []
    for i in range(0,m):
        for j in range(i+1,m):
            res.append((arr[i], arr[j]))
    return res



def scale_one(x):
    #归一化处理
    x[np.isinf(x)] = np.nan
    res = (x.T / (np.nansum(np.abs(x), axis=1) + 1e-20)).T
    return res



########################################################################
class MultipleAlphasAnalysis():
    def __init__(self, factor_wgts_df_dict):
        if not isinstance(factor_wgts_df_dict, dict): raise Exception("MultiFeatureAnalysis() input data should be dict type")
        self.factor_wgts_df_dict = factor_wgts_df_dict
        self.resample_dates = factor_wgts_df_dict[factor_wgts_df_dict.keys()[0]].index.values
        for i in self.factor_wgts_df_dict:
            self.factor_wgts_df_dict[i] = scale_one(self.factor_wgts_df_dict[i])

    def run(self):
        self.merge()
        self.plot()

    def merge(self):
        self.merge_dict = {}
        for i in self.factor_wgts_df_dict:
            self.merge_dict[i] = Merge(self.factor_wgts_df_dict[i], stat_info=False, plot=False)
            factor, returns, dates = self.merge_dict[i].run()

            bt = backtest.BackTest(factor,
                                        returns,
                                        dates,
                                        stat_info=False,
                                        plot=False)
            bt.run()
            self.merge_dict[i].alpha_pnl = bt.alpha_pnl
            self.merge_dict[i].alpha_cpnl = bt.alpha_cpnl
            self.merge_dict[i].alpha_sharpe = bt.alpha_sharpe
            self.merge_dict[i].IC_IR = bt.IC_IR
            self.merge_dict[i].alpha_drawdown = bt.alpha_drawdown


    def plot(self, is_oos_arr=None):     
        #alpha_cpnl
        plt.figure(figsize=(15,7))
        for i in self.merge_dict:
            alpha_cpnl = np.zeros(len(self.merge_dict[i].alpha_cpnl)+1)
            alpha_cpnl[1:] = self.merge_dict[i].alpha_cpnl
            alpha_cpnl_line = plt.plot(alpha_cpnl, linewidth=2, label=i)

        if not isinstance(self.resample_dates[0], str): dates = [str(i) for i in self.resample_dates]
        dates = self.resample_dates
        step = len(dates)/8
        space = [i for i in np.arange(len(dates)) if i%step==0]
        dates_str = [i.split(' ')[0] for i in dates[space]]
        if len(np.unique(dates_str)) <= 3:
            step = len(dates)/5
            space = [i for i in np.arange(len(dates)) if i%step==0]
            dates_str = [i for i in dates[space]]
        if is_oos_arr is not None:
            start = np.where(is_oos_arr==1)[0][0]
            for i in np.unique(is_oos_arr)[1:]:
                end = np.where(is_oos_arr==i)[0][-1]
                p = plt.axvspan(start, end, edgecolor='red', facecolor='grey', linewidth=1, alpha=0.2)
                start = end
        else:
            plt.grid()
        plt.xticks(space, dates_str)
        plt.legend(loc=2)
        plt.xlabel('Date')
        plt.ylabel('PNL')
        plt.title('Accumulated profits & loss')
        plt.show()
        time.sleep(0.5)


        gf = GridFigure(4, 1)
        # alpha_drawdown
        ax = gf.next_row()
        for i in self.merge_dict:
            alpha_drawdown = self.merge_dict[i].alpha_drawdown
            ax.fill_between(np.arange(len(alpha_drawdown)), np.zeros_like(alpha_drawdown), alpha_drawdown, alpha=0.5, label=i)
        ax.set(ylabel='Alpha Drawdown')
        ax.legend(loc='lower left')
        #plt.show()


        # 两两提升对比图
        combination_list = combination_2(self.merge_dict.keys())
        ax = gf.next_row()
        for i in range(len(combination_list)):
            alpha_cpnl_1 = self.merge_dict[combination_list[i][0]].alpha_cpnl
            alpha_cpnl_2 = self.merge_dict[combination_list[i][1]].alpha_cpnl
            diff = alpha_cpnl_1 - alpha_cpnl_2
            ax.fill_between(range(len(diff)), np.zeros_like(diff), diff, alpha=0.5, label="%s - %s" %(combination_list[i][0], combination_list[i][1]))
        ax.set(ylabel='cpnl_diff')
        ax.legend(loc='lower left')
        #plt.show()


        # 两两correlation
        rolling_period_length = 100
        combination_list = combination_2(self.merge_dict.keys())
        ax = gf.next_row()
        for i in range(len(combination_list)):
            alpha_pnl_1 = np.nan_to_num(self.merge_dict[combination_list[i][0]].alpha_pnl)
            alpha_pnl_2 = np.nan_to_num(self.merge_dict[combination_list[i][1]].alpha_pnl)
            rolling_corr = talib.CORREL(alpha_pnl_1, alpha_pnl_2, rolling_period_length)
            #rolling_corr = pd.DataFrame(alpha_pnl_1).rolling(rolling_period_length).corr(pd.DataFrame(alpha_pnl_2)).values.ravel()
            ax.fill_between(range(len(diff)), np.zeros_like(rolling_corr), rolling_corr, alpha=0.5, label="corr_%s(%s, %s)" %(rolling_period_length, combination_list[i][0], combination_list[i][1]))
        ax.set(ylabel='pnl correlation')
        ax.legend(loc='lower left')
        #plt.show()


        #截面correlation  
        rolling_period_length = 100
        combination_list = combination_2(self.merge_dict.keys())
        ax = gf.next_row()

        for i in range(len(combination_list)):
            rolling_corr = np.zeros(len(self.factor_wgts_df_dict[combination_list[i][0]]))
            for j in range(len(self.factor_wgts_df_dict[combination_list[i][0]])):
                rolling_corr[j] = np.corrcoef(self.factor_wgts_df_dict[combination_list[i][0]].iloc[j].values, self.factor_wgts_df_dict[combination_list[i][1]].iloc[j].values)[0,1]
            #rolling_corr = pd.DataFrame(alpha_pnl_1).rolling(rolling_period_length).corr(pd.DataFrame(alpha_pnl_2)).values.ravel()
            #ax.fill_between(range(len(rolling_corr)), np.zeros_like(rolling_corr), rolling_corr, alpha=0.5, label="corr_%s(%s, %s)" %(rolling_period_length, combination_list[i][0], combination_list[i][1]))
            #ax.fill_between(range(len(diff)), np.zeros_like(rolling_corr), rolling_corr, alpha=0.5, label="corr_%s(%s, %s)" %(rolling_period_length, combination_list[i][0], combination_list[i][1]))
            ax.fill_between(range(len(diff)), np.zeros_like(rolling_corr), rolling_corr, alpha=0.5, label="%s, %s" %(combination_list[i][0], combination_list[i][1]))
        ax.set(ylabel='cross section correlation')
        ax.legend(loc='lower left')
        gf.show()
        gf.close()










