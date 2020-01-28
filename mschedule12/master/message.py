
from .storage import Storage

class Message:
    """rpc暴露给客户端的接口"""
    def __init__(self):
        self.store = Storage()

    def reg(self, msg:dict):
        txt = "reg msg={}".format(msg)
        print(txt)
        ts = msg['timestamp']
        self.store.reg(msg['id'], msg['hostname'], msg['ips'])
        return txt

    def heartbeat(self, msg:dict):
        txt = "hb msg={}".format(msg)
        print(txt)
        ts = msg['timestamp']
        self.store.heartbeat(msg['id'], msg['hostname'], msg['ips'])
        return txt

    def pull_task(self, agent_id):
        #task_id, script, timeout = self.store.get_task_by_agentid(agent_id)
        return self.store.get_task_by_agentid(agent_id)

    def add_task(self, task:dict): # http json => ws json->dict => master dict
        id = self.store.add_task(task)
        return id

    def result(self, msg):  # 执行结果接口
        self.store.result(msg)
        return 'ack result'

    def agents(self):
        ret = self.store.get_agents()
        print(ret, '++++++++++++++++++++++++')
        return self.store.get_agents() # {'fdafasf':'node1'}

