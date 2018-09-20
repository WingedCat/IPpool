from GetIP.Getter import Getter
from WebService.WebServer import app
from TEST.TestIP import Tester
from multiprocessing import Process
import time

TEST_CYCLE = 20
GET_CYCLE = 20
TEST_ENABLE = True
GET_ENABLE = True

class Scheduler:
    def schedule_test(self,cycle = TEST_CYCLE):
        '''
        定时检测代理
        :param cycle: 检测间隔时间
        :return:
        '''
        tester = Tester()
        while True:
            print('测试开始...')
            tester.run()
            time.sleep(cycle)

    def schedule_get(self,cycle=GET_CYCLE):
        '''
        定时获取IP
        :param cycle: 获取间隔时间
        :return:
        '''
        getter = Getter()
        while True:
            print('开始获取IP...')
            getter.run()
            time.sleep(cycle)

    def run(self):
        '''
        总体调度
        :return:
        '''
        print('代理池开始运行...')
        if TEST_ENABLE:
            tester_process = Process(target=self.schedule_test())
            tester_process.start()

        if GET_ENABLE:
            getter_process = Process(target=self.schedule_get())
            getter_process.start()

if __name__=='__main__':
    s = Scheduler()
    s.run()