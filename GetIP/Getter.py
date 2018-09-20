from DB.RedisClient import RedisClient
from CrawerIP import Crawler

THRESHOLD = 500#数据库中最多存储500条IP
class Getter:
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_arrive_threshold(self):
        '''
        判断当前数据库中的IP条目数是否到达设置的阈值
        :return:
        '''
        if self.redis.count() >= THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('Getter Run...')
        if not self.is_arrive_threshold():
            #未到达阈值才继续获取
            '''
           调用Crawler类的crawl_*方法
           '''
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)

if __name__=='__main__':
    getter = Getter()
    getter.run()
