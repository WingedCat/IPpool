import requests
from pyquery import PyQuery as pq

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'}
def get_html(url):
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code==200:
            print("爬取%s成功"%url)
            return resp.text
    except Exception:
        print("爬取%s失败" % url)
        return

class ProxyCrawlerMetaclass(type):
    def __new__(cls, name,bases,attrs):
        count = 0
        attrs['__CrawlFunc__']=[]
        for k,v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass=ProxyCrawlerMetaclass):
    def get_proxies(self,callback):
        '''
        通过回调函数名执行对应的方法，返回获取到的所有代理
        :param callback: 回调函数名
        :return:
        '''
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            # print('get_proxies success')
            proxies.append(proxy)
        return proxies

    def crawl_66(self,page=4):
        for num in range(1,page+1):
            url = 'http://www.66ip.cn/{}.html'.format(num)
            html = get_html(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox  table  tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])

    def crawl_xici(self,page=4):
        for num in range(1,page+1):
            url = 'http://www.xicidaili.com/nn/{}'.format(num)
            html = get_html(url)
            if html:
                doc = pq(html)
                trs = doc('#ip_list tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(2)').text()
                    port = tr.find('td:nth-child(3)').text()
                    yield ':'.join([ip,port])
    def crawl_kuai(self,page=4):
        for num in range(1,page+1):
            url = 'https://www.kuaidaili.com/free/inha/{}/'.format(num)
            html = get_html(url)
            if html:
                doc = pq(html)
                trs = doc('#list tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])


if __name__=='__main__':
    c = Crawler()
    p = c.get_proxies('crawl_kuai')
    for item in p:
        print(item)