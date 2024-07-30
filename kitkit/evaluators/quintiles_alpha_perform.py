import os, yaml
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def drawdown(cpnl):
    _cpnl = cpnl * np.ones((cpnl.shape[0], cpnl.shape[0]))
    _cpnl = np.tril(_cpnl)
    max_cpnl = np.nanmax(_cpnl, axis=1)
    return cpnl - max_cpnl



def drawdown_period(cpnl):
    _cpnl = cpnl * np.ones((cpnl.shape[0], cpnl.shape[0]))
    _cpnl = np.tril(_cpnl)
    _cpnl = np.hstack((np.zeros((cpnl.shape[0],1)), _cpnl))
    max_cpnl = np.argmax(_cpnl, axis=1)
    return np.arange(len(cpnl)) - max_cpnl + 1


def Rsquared(y):
    # return R^2 where x and y are array-like
    from scipy.stats import linregress
    x = np.arange(len(y))
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    return r_value**2, x*slope + intercept


def scale_one(x):
    #归一化处理
    x[np.isinf(x)] = np.nan
    res = (x.T / (np.nansum(np.abs(x), axis=1) + 1e-20)).T
    return res


def equal_wgts(x):
    x = np.nan_to_num(x)
    x[x > 0] = 1
    x[x < 0] = -1
    return x


class QuintilesAlphaPerform():
    def __init__(self, dealObj, commission, cycle, quintiles_num, figure=True, signal_name=None, stat_info=True, output_dir=None):
        self.scaled_resample_wgts = dealObj.scaled_resample_wgts
        self.quintiles_num = quintiles_num
        self.cfg = {'Cycle': cycle, 'Quintiles': quintiles_num, 'Commission': commission, 'figure': figure, 'stat_info': stat_info, 'output_dir': output_dir}
        self.resample_return = dealObj.resample_return
        self.resample_dates = dealObj.resample_dates
        self.signal_name = signal_name


    def build(self):
        # origin signal
        self.stat_turnover()
        self.stat_pnl()
        self.stat_net_pnl()
        self.stat_sharpe()
        self.stat_drawdown()
        self.stat_drawdown_period()
        self.stat_anual()
        self.stat_IC()
        self.stat_Rsquared()


        # alpha signal
        self.stat_quintiles()
        self.stat_quintiles_pnl()
        self.stat_alpha_turnover()
        self.stat_alpha_pnl()
        self.stat_net_alpha_pnl()
        self.stat_alpha_sharpe()
        self.stat_alpha_drawdown()
        self.stat_alpha_drawdown_period()
        self.stat_net_alpha_sharpe()
        self.stat_net_alpha_drawdown()
        self.stat_net_alpha_drawdown_period()
        self.stat_alpha_Rsquared()
        self.stat_alpha_time_series_cpnl()
        self.stat_info()

        # figure
        self.plot()
        


    # ============================================ raw signal =================================================
    def stat_turnover(self):
        # raw signal turnover
        shift = np.zeros_like(self.scaled_resample_wgts) * np.nan
        shift[1:] = self.scaled_resample_wgts[:-1]
        self.turnover = np.nansum(np.nan_to_num(np.abs(self.scaled_resample_wgts - shift)), axis=1)
        self.avg_turnover = np.nanmean(self.turnover)



    #----------------------------------------------------------------------
    def stat_pnl(self):
        # raw signal pnl
        ret = self.resample_return * self.scaled_resample_wgts
        self.pnl = np.nan_to_num(np.nansum(ret, axis=1))
        self.cpnl = np.cumsum(self.pnl)


    #----------------------------------------------------------------------
    def stat_net_pnl(self):
        self.cost = self.cfg['Commission'] * self.turnover
        self.ccost = np.cumsum(self.cost)
        self.net_pnl = self.pnl - self.cost
        self.net_cpnl = np.cumsum(self.net_pnl)


    #----------------------------------------------------------------------
    def stat_anual(self):
        if self.cfg['Cycle'].upper() == '15MIN':
            self.net_anual_pnl = np.nanmean(self.net_pnl) * 252 * 16
        elif self.cfg['Cycle'].upper() == '60MIN':
            self.net_anual_pnl = np.nanmean(self.net_pnl) * 252 * 4
        elif self.cfg['Cycle'].upper() == '2HOUR':
            self.net_anual_pnl = np.nanmean(self.net_pnl) * 252 * 2
        elif self.cfg['Cycle'].upper() == 'DAY' or self.cfg['Cycle'] == '1DAY':
            self.net_anual_pnl = np.nanmean(self.net_pnl) * 252 
        else:
            raise Exception('stat_sharpe error! no match time frame')



    #----------------------------------------------------------------------
    def stat_sharpe(self):
        if self.cfg['Cycle'].upper() == '15MIN':
            self.sharpe =  np.sqrt(252 * 16) * np.nanmean(self.net_pnl) / np.nanstd(self.net_pnl)  
        elif self.cfg['Cycle'].upper() == '60MIN':
            self.sharpe =  np.sqrt(252 * 4) * np.nanmean(self.net_pnl) / np.nanstd(self.net_pnl) 
        elif self.cfg['Cycle'].upper() == '2HOUR':
            self.sharpe =  np.sqrt(252 * 2) * np.nanmean(self.net_pnl) / np.nanstd(self.net_pnl) 
        elif self.cfg['Cycle'].upper() == 'DAY' or self.cfg['Cycle'] == '1DAY':
            self.sharpe =  np.sqrt(252) * np.nanmean(self.net_pnl) / np.nanstd(self.net_pnl)  
        else:
            raise Exception('stat_sharpe error! no match time frame')


    #----------------------------------------------------------------------
    def stat_drawdown(self):
        self.drawdown = drawdown(self.net_cpnl)
        self.max_drawdown = round(np.abs(np.min(self.drawdown)), 4)


    #----------------------------------------------------------------------
    def stat_drawdown_period(self):
        self.drawdown_period = drawdown_period(self.net_cpnl)
        self.max_drawdown_period = int(np.max(self.drawdown_period))

    #----------------------------------------------------------------------
    def stat_Rsquared(self):
        self.r_squared, self.regress = Rsquared(self.net_cpnl)


    #----------------------------------------------------------------------
    def stat_IC(self):
        # alpha 的 Infomation Coefficience(这里用RankIC，spearman rank) 即某时点某因子在全部股票因子暴露值排名与其下期回报排名的截面相关系数。
        
        def rankdata(x):
            import scipy.stats as st
            tmp_x = x.copy() 
            idx = np.sum(~np.isnan(tmp_x), axis=1) == 0  #某行全为nan值
            tmp_x[idx, :] = 0
            #sz = np.sum(~np.isnan(x), axis=1)
            res = st.mstats.rankdata(tmp_x, axis=1)   #.T/sz.astype(float)).T
            res[np.isnan(x)] = np.nan
            return res

        if np.isnan(self.sharpe) or self.sharpe == 0: 
            self.IC = np.nan
            self.IC_IR = np.nan
            self.IC_arr = np.nan * np.zeros_like(self.resample_dates.shape)
            return 
        IC_arr = []
        rank_wgts = rankdata(self.scaled_resample_wgts)
        rank_return = rankdata(self.resample_return)
        #from scipy.stats import linregress
        for i in range(self.scaled_resample_wgts.shape[0]):
            #index_ = ~np.isnan(rank_wgts[i]) * ~np.isnan(rank_return[i])
            if np.isnan(rank_wgts[i]).all() or np.isnan(rank_return[i]).all():
                ic_val = np.nan
            else:
                ic_val = np.corrcoef(rank_wgts[i], rank_return[i])[0, 1]
            ##x = rank_wgts[i][index_] 
            ##y = rank_return[i][index_]
            ##slope, intercept, r_value, p_value, std_err = linregress(x, y) 
            IC_arr.append(ic_val)

        self.IC_arr = np.nan_to_num(IC_arr)
        self.IC = np.nanmean(IC_arr)
        self.IC_IR = np.nanmean(np.nan_to_num(IC_arr))/np.nanstd(np.nan_to_num(IC_arr))


    # ============================================ alpha signal ================================================= 
    def sort_quintiles(self, wgts, bottom, up):
        # 排序选择
        not_nan_num = - np.sum(np.isnan(wgts), axis=1) + wgts.shape[1]
        bottom_num = (np.round(bottom/100. * not_nan_num).astype(np.int) * np.ones_like(wgts).T).T   
        up_num = (np.round(up/100. * not_nan_num).astype(np.int) * np.ones_like(wgts).T).T               # 四舍五入, 然后进行类型转换 9.5 ---> 10. ---> 10
        rank_wgts = np.argsort(np.argsort(wgts, axis=1), axis=1).astype(np.float) + 1                #这里加1
        rank_wgts[np.isnan(wgts)] = np.nan
        res = np.ones_like(wgts)
        res[rank_wgts <= bottom_num] = np.nan
        res[rank_wgts > up_num] = np.nan
        return res



    #----------------------------------------------------------------------
    def stat_quintiles(self):
        quintiles_num=self.cfg['Quintiles']
        # 多分位测试
        if  quintiles_num == 10:
            self.quintiles_1 = self.sort_quintiles(self.scaled_resample_wgts, 0, 10)
            self.quintiles_2 = self.sort_quintiles(self.scaled_resample_wgts, 10, 20)
            self.quintiles_3 = self.sort_quintiles(self.scaled_resample_wgts, 20, 30)
            self.quintiles_4 = self.sort_quintiles(self.scaled_resample_wgts, 30, 40)
            self.quintiles_5 = self.sort_quintiles(self.scaled_resample_wgts, 40, 50)
            self.quintiles_6 = self.sort_quintiles(self.scaled_resample_wgts, 50, 60)
            self.quintiles_7 = self.sort_quintiles(self.scaled_resample_wgts, 60, 70)
            self.quintiles_8 = self.sort_quintiles(self.scaled_resample_wgts, 70, 80)
            self.quintiles_9 = self.sort_quintiles(self.scaled_resample_wgts, 80, 90)
            self.quintiles_10 = self.sort_quintiles(self.scaled_resample_wgts, 90, 100)
        elif quintiles_num == 5:
            """
            五分位测试
            多头值和空头值最大的20%， 20%-40%， 40%-60%，60-80%，80%-100%
            """
            self.quintiles_1 = self.sort_quintiles(self.scaled_resample_wgts, 0, 20)
            self.quintiles_2 = self.sort_quintiles(self.scaled_resample_wgts, 20, 40)
            self.quintiles_3 = self.sort_quintiles(self.scaled_resample_wgts, 40, 60)
            self.quintiles_4 = self.sort_quintiles(self.scaled_resample_wgts, 60, 80)
            self.quintiles_5 = self.sort_quintiles(self.scaled_resample_wgts, 80, 100)

        elif quintiles_num == 4:
            """
            4分位测试
            多头值和空头值最大的25%， 25%-50%， 50%-75%, 75%-100%
            """
            self.quintiles_1 = self.sort_quintiles(self.scaled_resample_wgts, 0, 2)
            self.quintiles_2 = self.sort_quintiles(self.scaled_resample_wgts, 25, 50)
            self.quintiles_3 = self.sort_quintiles(self.scaled_resample_wgts, 50, 75)
            self.quintiles_4 = self.sort_quintiles(self.scaled_resample_wgts, 75, 100)

        elif quintiles_num == 3:
            """
            3分位测试
            多头值和空头值最大的33%， 33%-66%, 66%-100%
            """
            self.quintiles_1 = self.sort_quintiles(self.scaled_resample_wgts, 0, 33)
            self.quintiles_2 = self.sort_quintiles(self.scaled_resample_wgts, 33, 67)
            self.quintiles_3 = self.sort_quintiles(self.scaled_resample_wgts, 67, 100)
        
        elif quintiles_num == 2:
            """
            2分位测试
            多头值和空头值最大的33%， 33%-66%, 66%-100%
            """
            self.quintiles_1 = self.sort_quintiles(self.scaled_resample_wgts, 0, 50)
            self.quintiles_2 = self.sort_quintiles(self.scaled_resample_wgts, 50, 100)

        else:
            raise Exception('')



    #----------------------------------------------------------------------
    def stat_quintiles_pnl(self):
        quintiles_num=self.cfg['Quintiles']
        #setattr(self, 'quintiles_%s_return' %i, scale_one(getattr(self, 'quintiles_%s' %i)) * self.OOS_resample_return)
        #setattr(self, 'quintiles_%s_pnl' %i, np.nan_to_num(np.nansum(getattr(self, 'quintiles_%s_return' %i), axis=1)) )
        if quintiles_num == 10:
            self.quintiles_1_return = scale_one(self.quintiles_1) * self.resample_return
            self.quintiles_2_return = scale_one(self.quintiles_2) * self.resample_return
            self.quintiles_3_return = scale_one(self.quintiles_3) * self.resample_return
            self.quintiles_4_return = scale_one(self.quintiles_4) * self.resample_return
            self.quintiles_5_return = scale_one(self.quintiles_5) * self.resample_return
            self.quintiles_6_return = scale_one(self.quintiles_6) * self.resample_return
            self.quintiles_7_return = scale_one(self.quintiles_7) * self.resample_return
            self.quintiles_8_return = scale_one(self.quintiles_8) * self.resample_return
            self.quintiles_9_return = scale_one(self.quintiles_9) * self.resample_return
            self.quintiles_10_return = scale_one(self.quintiles_10) * self.resample_return

            self.quintiles_1_pnl = np.nan_to_num(np.nansum(self.quintiles_1_return, axis=1)) 
            self.quintiles_2_pnl = np.nan_to_num(np.nansum(self.quintiles_2_return, axis=1)) 
            self.quintiles_3_pnl = np.nan_to_num(np.nansum(self.quintiles_3_return, axis=1)) 
            self.quintiles_4_pnl = np.nan_to_num(np.nansum(self.quintiles_4_return, axis=1))
            self.quintiles_5_pnl = np.nan_to_num(np.nansum(self.quintiles_5_return, axis=1)) 
            self.quintiles_6_pnl = np.nan_to_num(np.nansum(self.quintiles_6_return, axis=1)) 
            self.quintiles_7_pnl = np.nan_to_num(np.nansum(self.quintiles_7_return, axis=1)) 
            self.quintiles_8_pnl = np.nan_to_num(np.nansum(self.quintiles_8_return, axis=1)) 
            self.quintiles_9_pnl = np.nan_to_num(np.nansum(self.quintiles_9_return, axis=1))
            self.quintiles_10_pnl = np.nan_to_num(np.nansum(self.quintiles_10_return, axis=1)) 

        # 多分位测试
        elif quintiles_num == 5:
            """
            五分位测试
            多头值和空头值最大的20%， 20%-40%， 40%-60%，60-80%，80%-100%
            """
            self.quintiles_1_return = scale_one(self.quintiles_1) * self.resample_return
            self.quintiles_2_return = scale_one(self.quintiles_2) * self.resample_return
            self.quintiles_3_return = scale_one(self.quintiles_3) * self.resample_return
            self.quintiles_4_return = scale_one(self.quintiles_4) * self.resample_return
            self.quintiles_5_return = scale_one(self.quintiles_5) * self.resample_return

            self.quintiles_1_pnl = np.nan_to_num(np.nansum(self.quintiles_1_return, axis=1)) 
            self.quintiles_2_pnl = np.nan_to_num(np.nansum(self.quintiles_2_return, axis=1)) 
            self.quintiles_3_pnl = np.nan_to_num(np.nansum(self.quintiles_3_return, axis=1)) 
            self.quintiles_4_pnl = np.nan_to_num(np.nansum(self.quintiles_4_return, axis=1))
            self.quintiles_5_pnl = np.nan_to_num(np.nansum(self.quintiles_5_return, axis=1)) 

        elif quintiles_num == 4:
            """
            4分位测试
            多头值和空头值最大的25%， 25%-50%， 50%-75%, 75%-100%
            """
            self.quintiles_1_return = scale_one(self.quintiles_1) * self.resample_return
            self.quintiles_2_return = scale_one(self.quintiles_2) * self.resample_return
            self.quintiles_3_return = scale_one(self.quintiles_3) * self.resample_return
            self.quintiles_4_return = scale_one(self.quintiles_4) * self.resample_return

            self.quintiles_1_pnl = np.nan_to_num(np.nansum(self.quintiles_1_return, axis=1)) 
            self.quintiles_2_pnl = np.nan_to_num(np.nansum(self.quintiles_2_return, axis=1)) 
            self.quintiles_3_pnl = np.nan_to_num(np.nansum(self.quintiles_3_return, axis=1)) 
            self.quintiles_4_pnl = np.nan_to_num(np.nansum(self.quintiles_4_return, axis=1))
        elif quintiles_num == 3:
            """
            3分位测试
            多头值和空头值最大的33%， 33%-66%, 66%-100%
            """
            self.quintiles_1_return = scale_one(self.quintiles_1) * self.resample_return
            self.quintiles_2_return = scale_one(self.quintiles_2) * self.resample_return
            self.quintiles_3_return = scale_one(self.quintiles_3) * self.resample_return

            self.quintiles_1_pnl = np.nan_to_num(np.nansum(self.quintiles_1_return, axis=1)) 
            self.quintiles_2_pnl = np.nan_to_num(np.nansum(self.quintiles_2_return, axis=1)) 
            self.quintiles_3_pnl = np.nan_to_num(np.nansum(self.quintiles_3_return, axis=1)) 

        elif quintiles_num == 2:
            """
            2分位测试
            多头值和空头值最大的33%， 33%-66%, 66%-100%
            """
            self.quintiles_1_return = scale_one(self.quintiles_1) * self.resample_return
            self.quintiles_2_return = scale_one(self.quintiles_2) * self.resample_return

            self.quintiles_1_pnl = np.nan_to_num(np.nansum(self.quintiles_1_return, axis=1)) 
            self.quintiles_2_pnl = np.nan_to_num(np.nansum(self.quintiles_2_return, axis=1)) 

        else:
            raise Exception('')




    #----------------------------------------------------------------------
    def stat_alpha_pnl(self):
        quintiles_num=self.cfg['Quintiles']
        top_pnl = getattr(self, 'quintiles_' + str(quintiles_num) + '_pnl')
        bottom_pnl = getattr(self, 'quintiles_' + str(1) + '_pnl')
        self.alpha_pnl = 0.5*top_pnl - 0.5*bottom_pnl
        self.alpha_cpnl = np.cumsum(self.alpha_pnl)

    #----------------------------------------------------------------------
    def stat_net_alpha_pnl(self):
        self.alpha_cost = self.cfg['Commission'] * self.alpha_turnover_arr
        self.net_alpha_pnl = self.alpha_pnl - self.alpha_cost
        self.net_alpha_cpnl = np.cumsum(self.net_alpha_pnl)


    #----------------------------------------------------------------------
    def stat_alpha_turnover(self):
        quintiles_num=self.cfg['Quintiles']
        top_quintile = getattr(self, 'quintiles_' + str(quintiles_num))
        bottom_quintile = getattr(self, 'quintiles_' + str(1))


        self.top_bottom_quintile = scale_one(np.nan_to_num(top_quintile) - np.nan_to_num(bottom_quintile))
        shift = np.zeros_like(self.top_bottom_quintile) * np.nan
        shift[1:] = self.top_bottom_quintile[:-1]
        self.alpha_turnover_arr = np.nansum(np.nan_to_num(np.abs(self.top_bottom_quintile - shift)), axis=1)
        self.alpha_turnover = np.nanmean(self.alpha_turnover_arr)


        self.quantile_turnover = {}
        top_quintile = scale_one(equal_wgts(np.abs(top_quintile)))
        shift = np.zeros_like(top_quintile) * np.nan
        shift[1:] = np.nan_to_num(top_quintile)[:-1]
        self.quantile_turnover[quintiles_num] = np.nansum(np.abs(np.nan_to_num(top_quintile) - shift), axis=1)

        bottom_quintile = scale_one(equal_wgts(np.abs(bottom_quintile)))
        shift = np.zeros_like(bottom_quintile) * np.nan
        shift[1:] = np.nan_to_num(bottom_quintile)[:-1]
        self.quantile_turnover[1] = np.nansum(np.abs(np.nan_to_num(bottom_quintile) - shift), axis=1)
        #raise Exception()


    #----------------------------------------------------------------------
    def stat_alpha_sharpe(self):
        if self.cfg['Cycle'] == '15MIN' :
            self.alpha_sharpe =  np.sqrt(252 * 16) * np.nanmean(self.alpha_pnl)/np.nanstd(self.alpha_pnl)  
        elif self.cfg['Cycle'] == '60MIN':
            self.alpha_sharpe =  np.sqrt(252 * 4) * np.nanmean(self.alpha_pnl)/np.nanstd(self.alpha_pnl) 
        elif self.cfg['Cycle'] == '2HOUR':
            self.alpha_sharpe =  np.sqrt(252 * 2) * np.nanmean(self.alpha_pnl)/np.nanstd(self.alpha_pnl) 
        elif self.cfg['Cycle'] == 'DAY' or self.cfg['Cycle'] == '1DAY':
            self.alpha_sharpe =  np.sqrt(252) * np.nanmean(self.alpha_pnl)/np.nanstd(self.alpha_pnl)  
        else:
            raise Exception('Cycle error')


    #----------------------------------------------------------------------
    def stat_net_alpha_sharpe(self):
        if self.cfg['Cycle'] == '15MIN' :
            self.net_alpha_sharpe =  np.sqrt(252 * 16) * np.nanmean(self.net_alpha_pnl)/np.nanstd(self.net_alpha_pnl)  
        elif self.cfg['Cycle'] == '60MIN':
            self.net_alpha_sharpe =  np.sqrt(252 * 4) * np.nanmean(self.net_alpha_pnl)/np.nanstd(self.net_alpha_pnl) 
        elif self.cfg['Cycle'] == '2HOUR':
            self.net_alpha_sharpe =  np.sqrt(252 * 2) * np.nanmean(self.net_alpha_pnl)/np.nanstd(self.net_alpha_pnl) 
        elif self.cfg['Cycle'] == 'DAY' or self.cfg['Cycle'] == '1DAY':
            self.net_alpha_sharpe =  np.sqrt(252) * np.nanmean(self.net_alpha_pnl)/np.nanstd(self.net_alpha_pnl)  
        else:
            raise Exception('Cycle error')

            

    #----------------------------------------------------------------------
    def stat_alpha_drawdown(self):
        self.alpha_drawdown = drawdown(self.alpha_cpnl)
        self.alpha_max_drawdown = round(np.abs(np.min(self.alpha_drawdown)), 3)

    
    #----------------------------------------------------------------------
    def stat_alpha_drawdown_period(self):
        self.alpha_drawdown_period = drawdown_period(self.alpha_cpnl)
        self.alpha_max_drawdown_period = int(np.max(self.alpha_drawdown_period))


    #----------------------------------------------------------------------
    def stat_net_alpha_drawdown(self):
        self.net_alpha_drawdown = drawdown(self.net_alpha_cpnl)
        self.net_alpha_max_drawdown = round(np.abs(np.min(self.net_alpha_drawdown)), 3)

    
    #----------------------------------------------------------------------
    def stat_net_alpha_drawdown_period(self):
        self.net_alpha_drawdown_period = drawdown_period(self.net_alpha_cpnl)
        self.net_alpha_max_drawdown_period = int(np.max(self.net_alpha_drawdown_period))


    #----------------------------------------------------------------------
    def stat_alpha_Rsquared(self):
        self.alpha_Rsquared, self.alpha_regress = Rsquared(self.alpha_cpnl)


    #----------------------------------------------------------------------
    def stat_alpha_time_series_cpnl(self):
        quintiles_num=self.cfg['Quintiles']
        top_return = getattr(self, 'quintiles_' + str(quintiles_num) + '_return')
        bottom_return = getattr(self, 'quintiles_' + str(1) + '_return')
        ts_return = 0.5 * np.nan_to_num(top_return) - 0.5 * np.nan_to_num(bottom_return)
        self.ts_cpnl = np.cumsum(np.nan_to_num(ts_return), axis=0)




    def stat_info(self):
        self.alpha_return = self.alpha_cpnl[-1]

        self.indicators = {}
        
        self.indicators["Start"] = str(self.resample_dates[0])
        self.indicators["End"] = str(self.resample_dates[-1])
        self.indicators['Cycle']= self.cfg['Cycle']
        self.indicators['Quintiles']= self.cfg['Quintiles']
        self.indicators['Commission']= self.cfg['Commission']
        # ===== origin =====
        self.indicators['Returns'] = round(float(self.cpnl[-1]), 2)
        self.indicators['Net Returns'] = round(float(self.net_cpnl[-1]), 2)
        self.indicators['Commission'] = round(float(self.ccost[-1]), 2)
        self.indicators['Sharpe'] = round(float(self.sharpe), 2)
        self.indicators['Turnover'] = round(float(self.avg_turnover), 2)
        self.indicators['Max Drawdown'] = round(float(self.max_drawdown), 2)
        self.indicators['Max DrawdownPeriod'] = self.max_drawdown_period
        self.indicators['Rsquared'] = round(float(self.r_squared), 2)
        self.indicators['IC'] = round(float(self.IC), 2)
        self.indicators['IC IR'] =round(float(self.IC_IR ), 2)


        # ===== alpha =====
        self.indicators["Alpha Turnover"] = round(float(self.alpha_turnover), 2)
        self.indicators["Alpha Returns"] = round(float(self.alpha_cpnl[-1]), 2)
        self.indicators["Alpha Net Returns"] = round(float(self.net_alpha_cpnl[-1]), 2)
        self.indicators["Alpha Sharpe"] = round(float(self.alpha_sharpe), 2)
        self.indicators["Alpha Net Sharpe"] = round(float(self.net_alpha_sharpe), 2)
        self.indicators["Alpha Max Drawdown"] = round(float(self.alpha_max_drawdown), 2)
        self.indicators["Alpha Max DrawdownPeriod"] = self.alpha_max_drawdown_period
        self.indicators["Alpha Net Max Drawdown"] = round(float(self.net_alpha_max_drawdown), 2)
        self.indicators["Alpha Net Max DrawdownPeriod"] = self.net_alpha_max_drawdown_period
        self.indicators["Alpha Rsquared"] = round(float(self.alpha_Rsquared), 2)

        print('[AlphaPerform] start:%s end:%s' %(self.resample_dates[0], self.resample_dates[-1]))
        self.stat_df = pd.DataFrame(self.indicators, index=[" "])
        if self.cfg['stat_info']: print(self.stat_df)

        if self.cfg['output_dir'] is not None:
            with open(os.path.join(self.cfg['output_dir'], 'quintiles_alpha_perform.yaml'), 'w') as f:
                yaml.dump(self.indicators, f, encoding='unicode', sort_keys=False)




    # def plot(self):
    #     figure = plt.figure(figsize=(18,10))
    #     quintiles_num = self.cfg["Quintiles"]
    #     for i in range(1, quintiles_num+1):
    #         q_pnl = getattr(self, 'quintiles_' + str(i) + '_pnl')
    #         tmp = np.zeros(len(q_pnl)+1)
    #         tmp[1:] = np.cumsum(q_pnl)
    #         signal_line = plt.plot(tmp, '-', linewidth=1, label='quintiles_' + str(i))

    #     alpha = np.zeros(len(self.alpha_cpnl)+1)
    #     alpha[1:] = self.alpha_cpnl
    #     alpha_line = plt.plot(alpha, color='r', linewidth=2, label='alpha')

    #     dates = self.resample_dates
    #     step = len(dates)/8
    #     space = [i for i in np.arange(len(dates)) if i%step==0]
    #     dates_str = [i.split(' ')[0] for i in dates[space]]
    #     if len(np.unique(dates_str)) <= 3:
    #         step = int(len(dates)/5)
    #         space = [i for i in np.arange(len(dates)) if i%step==0]
    #         dates_str = [i for i in dates[space]]
    #     plt.xticks(space, dates_str)
    #     #plt.xlabel('Date')
    #     plt.ylabel('PNL')
    #     plt.title(str(quintiles_num) + ' quintiles profits & loss')
    #     plt.legend(loc=2)
    #     plt.grid()
    #     plt.show()



    # ============================================== plot ====================================================
    def plot(self, is_oos_arr=None, title=None):
        if not self.cfg['figure']: return
        # 2 合 1绘图
        #import matplotlib.dates as mdates
        #from matplotlib.widgets import MultiCursor
        #import seaborn as sns 
        #sns.set(style='white')

        #dailypnl = np.nansum(self.pnl[sidx:eidx, :], axis=1)
        #dailypnl = np.nan_to_num(dailypnl)
        #a = 1 - np.nansum(self.wgts[di,:])
        #cdailypnl = np.cumsum(dailypnl)
        #dts = np.array([mdates.strpdate2num('%Y-%m-%d %H:%M:%S')(str(dt)) for dt in self.resample_dates])
        #sns.set_style("darkgrid")
        figure = plt.figure(figsize=(13,18))
        rect0 = [0.1, 0.675, 0.8, 0.275]
        rect1 = [0.1, 0.55, 0.8, 0.085]
        rect2 = [0.1, 0.175, 0.8, 0.275]
        rect3 = [0.1, 0.05, 0.8, 0.085]
        sub0 = plt.axes(rect0)
        sub1 = plt.axes(rect1)
        sub2 = plt.axes(rect2)
        sub3 = plt.axes(rect3)


        # ======================# ======================# ======================# ======================
        ax0 = plt.sca(sub0)

        # if self.cfg['Commission'] != 0.:
        #     net_alpha_cpnl = np.zeros(len(self.net_alpha_cpnl)+1)
        #     net_alpha_cpnl[1:] = self.net_alpha_cpnl
        #     net_alpha_cpnl_line = plt.plot(net_alpha_cpnl, color='g', linewidth=1.5, label='net alpha')
        #     plt.ylabel('net alpha')
        # else:
        #     alpha_cpnl = np.zeros(len(self.alpha_cpnl)+1)
        #     alpha_cpnl[1:] = self.alpha_cpnl
        #     alpha_cpnl_line = plt.plot(alpha_cpnl, color='r', linewidth=1.5, label='alpha')
        #     plt.ylabel('alpha')

        cpnl = np.zeros(len(self.cpnl)+1)
        cpnl[1:] = self.cpnl
        pnl_line = plt.plot(cpnl, color='b', linewidth=1.5, label="cpnl")
        plt.ylabel('cpnl')

        net_cpnl = np.zeros(len(self.net_cpnl)+1)
        net_cpnl[1:] = self.net_cpnl
        pnl_line = plt.plot(net_cpnl, color='r', linewidth=1.5, label="net_cpnl")


        if title is None and self.signal_name is None:
            plt.title('Accumulated profits & loss')
        elif self.signal_name is not None:
            plt.title(self.signal_name)
        else:
            plt.title(title)
        if not isinstance(self.resample_dates[0], str): dates = [str(i) for i in self.resample_dates]
        
        dates = self.resample_dates
        step = len(dates)/8
        space = [i for i in np.arange(len(dates)) if i%step==0]
        dates_str = [i.split(' ')[0] for i in dates[space]]
        if len(np.unique(dates_str)) <= 3:
            step = int(len(dates)/5)
            space = [i for i in np.arange(len(dates)) if i%step==0]
            dates_str = [i for i in dates[space]]
        if is_oos_arr is not None:
            start = np.where(is_oos_arr==1)[0][0]
            for i in np.unique(is_oos_arr)[1:]:
                end = np.where(is_oos_arr==i)[0][-1]
                p = plt.axvspan(start, end, edgecolor='red', facecolor='grey', linewidth=1.5, alpha=0.2)
                start = end
        plt.grid()
        plt.legend(loc=2)
        plt.xticks(space, dates_str)

        # ======================# ======================# ======================# ======================
        ax1 = plt.sca(sub1)
        plt.fill_between(np.arange(len(self.drawdown)), np.zeros_like(self.drawdown), self.drawdown, color='b', alpha=0.5, label='drawdown')
        plt.grid()
        plt.ylabel("Alpha Drawdown")
        plt.legend(loc=2)


        # ======================# ======================# ======================# ======================  
        # alpha PNL
        ax2 = plt.sca(sub2)
        quintiles_num = self.cfg["Quintiles"]
        for i in range(1, quintiles_num+1):
            q_pnl = getattr(self, 'quintiles_' + str(i) + '_pnl')
            tmp = np.zeros(len(q_pnl)+1)
            tmp[1:] = np.cumsum(q_pnl)
            signal_line = plt.plot(tmp, '-', linewidth=1, label='quintiles_' + str(i))

        alpha = np.zeros(len(self.alpha_cpnl)+1)
        alpha[1:] = self.alpha_cpnl
        alpha_line = plt.plot(alpha, color='b', linewidth=2, label='alpha')

        net_alpha = np.zeros(len(self.net_alpha_cpnl)+1)
        net_alpha[1:] = self.net_alpha_cpnl
        net_alpha_line = plt.plot(net_alpha, color='r', linewidth=2, label='net_alpha')


        if self.cfg['Commission'] != 0.:
            net_alpha_cpnl = np.zeros(len(self.net_alpha_cpnl)+1)
            net_alpha_cpnl[1:] = self.net_alpha_cpnl


        dates = self.resample_dates
        step = len(dates)/8
        space = [i for i in np.arange(len(dates)) if i%step==0]
        dates_str = [i.split(' ')[0] for i in dates[space]]
        if len(np.unique(dates_str)) <= 3:
            step = int(len(dates)/5)
            space = [i for i in np.arange(len(dates)) if i%step==0]
            dates_str = [i for i in dates[space]]
        plt.xticks(space, dates_str)
        #plt.xlabel('Date')
        plt.ylabel('PNL')
        plt.title(str(quintiles_num) + ' quintiles profits & loss')
        plt.grid()
        plt.legend(loc=2)


        # ======================# ======================# ======================# ======================
        # 绘制分位数图
        plt.sca(sub3)
        if self.cfg['Commission'] != 0.:
            plt.fill_between(np.arange(len(self.net_alpha_drawdown)), np.zeros_like(self.net_alpha_drawdown), self.net_alpha_drawdown, color='g', alpha=0.5, label='net_alpha_drawdown')
        else:
            plt.fill_between(np.arange(len(self.alpha_drawdown)), np.zeros_like(self.alpha_drawdown), self.alpha_drawdown, color='r', alpha=0.5, label='alpha_drawdown')


        if self.cfg['output_dir'] is not None:
            figure.savefig(os.path.join(self.cfg['output_dir'], 'quintiles_alpha_perform.jpg'))

        plt.show()


