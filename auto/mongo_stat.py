from pymongo import MongoClient
import pymongo
from tqdm import tqdm

"""
1. 每个layer的documents总数量，完成数量，未完成数量
2. 
"""
class Stats():
    def __init__(self, db_host, db_port, db_name):
        self.config = Munch()
        self.config.db_host = db_host
        self.config.db_port = db_port
        self.config.db_name = db_name
        
    def connect_mongodb(self):
        try:
            client = MongoClient(self.config.db_host, self.config.db_port)
            db = client[self.config.db_name]
        except Exception, e:
            print e, 'Connect to mongodb error'
        return db
    
    def run(self):
        for i in [1]:
            cursor = db['layer%s' %i].find({"IS_backtest": "Done"})
            print 'layer%s IS backtest num: %s' %(i, cursor.count())
            df = pd.DataFrame()
            tmp = []
            for j in tqdm(cursor, desc='%s' %cursor.count()):
                tmp.append(j)
        return tmp
    
    
    

                bar_length = 30
                percent = 1. * self.queue.qsize() / self.config.queue_size
                hashes = '#' * int(percent * bar_length)
                spaces = ' ' * (bar_length - len(hashes))
                sys.stdout.write("\r%s queue volume: %s/%s [%s] %d%% (%s/s)" % (time.strftime('%H:%M'),
                                                                      self.queue.qsize(), self.config.queue_size,
                                                                       hashes + spaces, percent * 100,
                                                                       np.round((q_num[0]-q_num[-1])/(q_time[-1]-q_time[0]+1e-10), 2)))
                sys.stdout.flush()
                time.sleep(0.5)

                
r = Report(db_host='127.0.0.1', db_port=27017, db_name='Machine')
db = r.connect_mongodb()
a = r.run()