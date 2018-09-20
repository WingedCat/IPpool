from flask import Flask,g
from DB.RedisClient import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>Welcome!</h2>'

@app.route('/get')
def get_proxy():
    '''
    随机获取代理
    :return: 随机代理
    '''
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    '''
    获得数据库中的代理总量
    :return: 代理总数
    '''
    print('get counts()')
    conn = get_conn()
    return str(conn.count())

if __name__=='__main__':
    app.run()