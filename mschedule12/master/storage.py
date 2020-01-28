from .agent import Agent
from .task import Task
import uuid
from common.state import *

class Storage:
    """负责agents、tasks存储，必要时实现持久化"""

    def __init__(self):
        self.agents = {} # 注册的agent的字典
        self.tasks = {} # 任务的字典

    def reg(self, id, hostname, ip):
        if id not in self.agents.keys():
            self.agents[id] = Agent(id, hostname, ip)
        else:
            agent = self.agents[id]
            agent.ip = ip
            agent.hostname = hostname

    def heartbeat(self, id, hostname, ip): # heartbeat id,timestamp # 告诉你我刚才来过，说明我是ok的
        if id not in self.agents.keys():
            self.agents[id] = Agent(id, hostname, ip)
        else:
            agent = self.agents[id]
            agent.ip = ip
            agent.hostname = hostname

    def add_task(self, task:dict): # new task
        id = uuid.uuid4().hex

        t = Task(id, **task)
        t.targets = {agent_id:self.agents[agent_id] for agent_id in t.targets} #['id1', 'id2']

        # 加入任务列表
        self.tasks[t.id] = t

        return t.id

    def iter_tasks(self, states={WAITING, RUNNING}):
        # for task in self.tasks.values():
        #     if task.state in states:
        #         yield task
        yield from (task for task in self.tasks.values() if task.state in states)

    def get_task_by_agentid(self, agent_id):
        for task in self.iter_tasks():
            if agent_id in task.targets.keys(): # 此agent是可以执行这个任务的
                agent = self.agents[agent_id]
                #if agent.state == WAITING:
                if task.id not in agent.outputs: # 没有领取过
                    agent.outputs[task.id] = None

                    task.state = RUNNING
                    agent.state = RUNNING

                    return task.id, task.script, task.timeout


    def result(self, msg:dict):
        agent_id = msg['id']
        agent = self.agents[agent_id]

        agent.outputs[msg['task_id']] = {
            'code':msg['code'],
            'output':msg['output']
        }

        agent.state = WAITING

    def get_agents(self):
        return {agent.id:agent.hostname for agent in self.agents.values()}

