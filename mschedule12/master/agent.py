import datetime
from common.state import *

class Agent:
    """客户端注册后的信息需要封装，提供一个信息存储的类，数据存储在类的实例中"""
    def __init__(self, id, hostname, ip):
        self.regtime = datetime.datetime.now() # 一个客户端发来的；用服务器自己的时间
        self.id = id
        self.hostname = hostname
        self.ip = ip
        self.state = WAITING
        self.outputs = {}
        # 每一个agent执行任务，如果你想遍历他的所有任务及结果
        # {task_id:{code:0, output:'node1'}}


    def __repr__(self):
        return '<Agent {} {} {}>'.format(self.id, self.hostname, self.ip)


