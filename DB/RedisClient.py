import redis
from random import choice

MAX_SCORE = 100
MIN_SCORE = 0
INITAL_SCORE = 10
HOST = 'localhost'
PORT = 6379
DB_NUM=4
PASSWORD = None
KEY = 'proxies'


class RedisClient:
    def __init__(self,host=HOST,pwd=PASSWORD,port=PORT):
        '''
        初始化，连接redis
        :param host: Redis 地址
        :param pwd: Redis 密码
        :param port: Redis 端口
        '''
        self.db = redis.StrictRedis(host=host,port=port,password=pwd,decode_responses=True,db=DB_NUM)

    def add(self,proxy,score=INITAL_SCORE):
        '''
        添加代理
        :param proxy: 待添加代理
        :param score: 标识的分数
        :return:
        '''
        if not self.db.zscore(KEY,proxy):
            return self.db.zadd(KEY,score,proxy)

    def random(self):
        '''
        随机获取代理，首先获取标识分数最高的，如果不存在则按照排序进行获取
        :return:
        '''
        result = self.db.zrevrange(KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(KEY,MIN_SCORE,MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                print('无代理可获取')
                return None
    def decrease(self,proxy):
        '''
        将指定代理的标识分数减1，如果标识值小于MIN_SCORE则将它从redis中移除
        :param proxy:
        :return:
        '''
        score = self.db.zscore(KEY,proxy)
        if score and score > MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(KEY,proxy,-1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(KEY,proxy)

    def exists(self,proxy):
        '''
        判断代理是否存在
        :return:
        '''
        return not self.db.zscore(KEY,proxy)==None

    def max(self,proxy):
        '''
        如果新代理检测可以使用在将标识值设置为MAX_SCORE
        :param proxy: 新代理
        :return:
        '''
        print('新代理',proxy,'可用,设置为',MAX_SCORE)
        return self.db.zadd(KEY,MAX_SCORE,proxy)

    def count(self):
        '''
        返回当前数据库中的代理总数
        :return:
        '''
        return self.db.zcard(KEY)

    def all(self):
        '''
        返回所有的代理，用于检测
        :return:
        '''
        return self.db.zrangebyscore(KEY,MIN_SCORE,MAX_SCORE)