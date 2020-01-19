from numpy import random
random.seed(20170605)
import copy


"""
GA_setting:
    generation: 50  #遗传代数
    popsize: 20      #种群大小
    chrosize: 10     #编码长度
    crossrate: 0.9    #交叉率
    mutationrate: 0.5    #变异率


"""
class GeneticAlgorithm():
    """
    GA 算法工具箱
    """
    def __init__(self, param_dict, generation, popsize, chrosize, crossrate, mutationrate, func):
        """
        generation: 遗传代数
        popsize: 种群大小
        chrosize： 编码长度
        crossrate: 交叉率
        mutationrate: 变异率
        * 算法默认使用了单点交叉, 赌轮盘选择, 精英策略 
        """  
        print 'genetic_algorithm initialized(generation=%s, popsize=%s)' %(generation, popsize)     
        self.param_dict = param_dict
        self.generation = generation
        self.popsize = popsize
        self.chrosize = chrosize
        self.crossrate = crossrate
        self.mutationrate = mutationrate
        self.func = func

    def initialpop(self):
        pop = random.randint(0,2,size =(self.popsize,self.chrosize))
        return pop


    def convert_param_type(self, param_dict):
        for j in param_dict:
            if 'Type' not in self.param_dict[j]:
                raise Exception('no type of param_dict')
            if self.param_dict[j]['Type'] == 'int':
                param_dict[j] = [int(i) for i in param_dict[j]]
            elif self.param_dict[j]['Type'] == 'float':
                param_dict[j] = [round(float(i),2) for i in param_dict[j]]
            else:
                raise Exception('no type of param_dict')
        return param_dict


    def run(self):
        elite_mode = True
        self.speed_mode = True
        declist, nextdeclist = {}, {}
        popbest, parambest = {}, {}

        import collections
        def tree():
            return collections.defaultdict(tree)
        self.fitness_record = tree()


        self.fit_best_record, self.pop_best_record, self.param_best_record = [], [], [] #每代最优个体对应的适应值, 二进制, 十进制
        pop = {}
        for id_ in self.param_dict:
            pop[id_] = self.initialpop()   #种群初始化


        for i in tqdm(range(self.generation)):
            #process_bar(i, self.generation, prefix_desc='generation')
            for j in self.param_dict:
                declist[j] =self.get_declist(pop[j], self.param_dict[j]['Start'], self.param_dict[j]['Stop'])#解码
            declist = self.scale_one(declist)
            fitvalue = self.get_fitness(declist, self.func)#适应度函数
            loc = fitvalue.index(max(fitvalue))#最高适应度的位置
            #选择适应度函数最高个体
            for j in self.param_dict:
                popbest[j] = pop[j][loc]

                popbest[j] =copy.deepcopy(popbest[j])                  #对popbest进行深复制，以为后面精英选择做准备
                parambest[j]= declist[j][loc]                          #最高适应度

            fitbest = max(fitvalue)                                     #保存每代最高适应度值
            
            self.fit_best_record.append(fitbest)
            self.pop_best_record.append(popbest.copy())
            self.param_best_record.append(parambest.copy())
            print 'best fitness', self.fit_best_record[-1]
            if len(self.fit_best_record)>=5 and len(np.unique(self.fit_best_record[-5:])) == 1: break
            ################################ 快速模式, 在某一代参数全部相同, 迭代结束条件
            if self.speed_mode is True:
                cond = []
                for j in declist:
                    cond.append(len(np.unique(declist[j])))  
                if len(np.unique(cond)) == 1 and cond[0] == 1: 
                    #print 'iteration satisfy condition and finish', declist, 'best', parambest
                    break
            ################################进行算子操作，并不断更新pop
            for j in self.param_dict:
                pop[j] = self.selection(pop[j],fitvalue)  #选择

                pop[j] = self.crossover(pop[j]) # 交叉

                pop[j] = self.mutation(pop[j])  #变异


            if elite_mode is False: continue
            ################################精英策略前的准备
            #对变异之后的pop，求解最大适应度
            for j in self.param_dict:
                nextdeclist[j] = self.get_declist(pop[j], self.param_dict[j]['Start'], self.param_dict[j]['Stop']) 
            nextdeclist = self.scale_one(nextdeclist)
            nextfitvalue =self.get_fitness(nextdeclist, self.func)        
            nextbestfit = max(nextfitvalue)
            ################################精英策略
            #比较深复制的个体适应度和变异之后的适应度
            pop = self.elitism(pop,popbest,nextbestfit,fitbest,nextfitvalue)



    def scale_one(self, declist):
        #参数归一化
        scaled_declist = {}
        _sum = np.sum(declist.values())
        for i in declist:
            scaled_declist[i] = declist[i]/_sum
        return scaled_declist


    def get_fitness(self, param_dict, func):
        fitness = []
        for i in xrange(self.popsize):
            #process_bar(i, self.popsize, prefix_desc='fitness')
            one_param_dict = {}
            for j in param_dict:
                one_param_dict[j] = param_dict[j][i]

            fitness_value = self.efficient(one_param_dict, func)
            fitness.append(fitness_value)
        return fitness


    def efficient(self, one_param_dict, func):
        for k in self.fitness_record:
            _param_dict = self.fitness_record[k]['param']
            _param_values = np.array([_param_dict.get(j, np.nan) for j in one_param_dict.keys()])
            if np.sum(_param_values - np.array(one_param_dict.values())) == 0:
                return self.fitness_record[k]['values']  #.copy()
        fitness_value = func(one_param_dict)
        id_ = str(len(self.fitness_record)+1)
        self.fitness_record[id_]['param'] = one_param_dict
        self.fitness_record[id_]['values'] = fitness_value
        return fitness_value



    #输入参数为上一代的种群，和上一代种群的适应度列表
    def selection(self, popsel, fitvalue):
        # 这里使用了轮盘赌选择（Roulette Wheel Selection ）
        # 如果使用排序选择算法, 需要rank值来替代fitvalue的目标函数值
        # "排序选择将使所有个体都有将会被选择。但是这样也会导致种群不容易收敛，因为最好的个体与其他个体的差别减小。"
        new_fitvalue = []
        totalfit = sum(fitvalue)
        accumulator = 0.0
        for val in fitvalue: 
            #对每一个适应度除以总适应度，然后累加，这样可以使适应度大
            #的个体获得更大的比例空间。
            new_val =(val*1.0/totalfit)            
            accumulator += new_val
            new_fitvalue.append(accumulator)            
        ms = []
        for i in xrange(self.popsize):
            #随机生成0,1之间的随机数
            ms.append(random.random()) 
        ms.sort() #对随机数进行排序
        fitin = 0
        newin = 0
        newpop = popsel
        while newin < self.popsize:
            #随机投掷，选择落入个体所占轮盘空间的个体
            if(ms[newin] < new_fitvalue[fitin]):
                newpop[newin] = popsel[fitin]
                newin = newin + 1
            else:
                fitin = fitin + 1
        #适应度大的个体会被选择的概率较大
        #使得新种群中，会有重复的较优个体
        pop = newpop
        return pop


    def crossover(self, pop):
        # 这里使用单点交叉
        # 对于两点交叉, 均匀交叉和算术交叉, TODO
        for i in xrange(self.popsize-1):
            #近邻个体交叉，若随机数小于交叉率
            if(random.random()<self.crossrate):
                #随机选择交叉点
                singpoint =random.randint(0,self.chrosize)
                temp1 = []
                temp2 = []
                #对个体进行切片，重组
                temp1.extend(pop[i][0:singpoint])
                temp1.extend(pop[i+1][singpoint:self.chrosize])
                temp2.extend(pop[i+1][0:singpoint])
                temp2.extend(pop[i][singpoint:self.chrosize])
                pop[i]=temp1
                pop[i+1]=temp2
        return pop 
    

    def mutation(self, pop):
        for i in xrange(self.popsize):
            #反转变异，随机数小于变异率，进行变异
            if (random.random()< self.mutationrate):
                mpoint = random.randint(0,self.chrosize-1)
                #将随机点上的基因进行反转。
                if(pop[i][mpoint]==1):
                    pop[i][mpoint] = 0
                else:
                    pop[mpoint] =1
        return pop


    def elitism(self,pop,popbest,nextbestfit,fitbest,nextfitvalue):
        #输入参数为上一代最优个体，变异之后的种群，
        #上一代的最优适应度，本代最优适应度。这些变量是在主函数中生成的。
        if nextbestfit-fitbest <0:  
            #满足精英策略后，找到最差个体的索引，进行替换。
            pop_worst =nextfitvalue.index(min(nextfitvalue))
            for j in pop:
                pop[j][pop_worst] = popbest[j]
        return pop


    #对十进制进行转换到求解空间中的数值
    def get_declist(self,chroms, xrangemax, xrangemin):
        step =(xrangemax - xrangemin)/float(2**self.chrosize-1)
        chroms_declist =[]
        for i in xrange(self.popsize):
            chrom_dec =xrangemin+step*self.chromtodec(chroms[i])  
            chroms_declist.append(chrom_dec)
        return chroms_declist
    

    #将二进制数组转化为十进制
    def chromtodec(self,chrom):
        m = 1
        r = 0
        for i in xrange(self.chrosize):
            r = r + m * chrom[i]
            m = m * 2
        return r


