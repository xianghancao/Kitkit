
## Update
### v1.0 Feb 7, 2020 
 初步完成了向量方式的回测，统计和绘图。
### v1.1.0 Feb 14, 2020 
 完成了自动搜索策略的功能，包括分布式队列，生成策略，计算策略和存储策略等。
### v1.1.1  Feb 25, 2020 
 evaluators/alpha_perform.py 增加了原始收益率的计算和绘图。
### v1.1.2 Mar 11, 2020 
 修改了auto下面task_queue.py和worker.py连接mongodb的方式
### v1.1.3 Mar 11, 2020 
 增加了negative运算符，修改了Auto下的worker，只回测信号值为正的信号
### v1.1.4 Mar 11, 2020
增加了benchmark_alpha_perform.py, 定义alpha为相对于基准收益的超额收益
增加了quintiles_alpha_perform.py, 定义alpha为Top分位数-bottom分位数收益
删除alpha_perform.py
### v1.1.5 Mar 12, 2020
增加了数据填充方法clean.py