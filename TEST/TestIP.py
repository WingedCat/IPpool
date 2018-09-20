import aiohttp
import asyncio
import time
from aiohttp import ClientError
from DB.RedisClient import RedisClient

TEST_URL = 'http://www.baidu.com'#测试网址，自定义修改
BATCH_SIZE = 100#一次测试的代理数目

class Tester:
    def __init__(self):
        self.redis = RedisClient()

    async def test_proxy(self,proxy):
        '''
        测试指定的代理
        :param proxy: 待测试的代理
        :return:
        '''
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('UTF-8')
                test_proxy = 'http://'+proxy
                print('测试:',proxy)
                async with session.get(TEST_URL,proxy=test_proxy,timeout=5) as resp:
                    if resp.status == 200:
                        self.redis.max(proxy)#检测到代理可用，将标识分数设置为MAX_SCORE
                    else:
                        self.redis.decrease(proxy)#代理不可用，标识分数减1
            except (AttributeError, TimeoutError, ClientError, aiohttp.ClientConnectorError):
                self.redis.decrease(proxy)#代理不可用，标识分数减1

    def run(self):
        '''
        测试main方法
        :return:
        '''
        print('开始测试...')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            #批量测试
            for i in range(0,len(proxies),BATCH_SIZE):
                test_proxies = proxies[i:i+BATCH_SIZE]#获取测试代理
                tasks = [self.test_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试错误',e.args)
