import zerorpc
# from .config import MASTER_URL
from .message import Message
from threading import Event, Thread
from utils import getlogger
from .executor import Executor
from common.state import *

logger = getlogger(__name__, 'o:/agent.cm.log')


class ConnectionManage: # client
    def __init__(self, url, myidpath):
        self.client = zerorpc.Client()
        self.event = Event()
        self.message = Message(myidpath)
        self.url = url

        self.__result = None
        self.state = WAITING

        self.executor = Executor()

    def __exec(self, task):
        task_id, script, timeout = task
        code, text = self.executor.run(script, timeout) # (code,text)

        self.__result = task_id, code, text
        self.state = SUCCESSFUL if code == 0 else FAILED


    def start(self, interval=5):
        while not self.event.wait(1):
            try:
                self.client.connect(self.url)

                ack = self.client.reg(self.message.reg()) # server的reg
                # if ack is None:
                #     raise Exception()

                while not self.event.wait(interval): # 心跳
                    self.client.heartbeat(self.message.heartbeat())

                    if self.state in {SUCCESSFUL, FAILED}: # done
                        ack = self.client.result(self.message.result(*self.__result)) # rpc服务端的result接口
                        logger.info('{}'.format(self.__result))
                        self.__result = None
                        self.state = WAITING

                    # 领任务
                    # 执行？同步执行？异步执行？线程
                    if self.state == WAITING:
                        task = self.client.pull_task(self.message.id)
                        if task:
                            self.state = RUNNING
                            Thread(target=self.__exec, args=(task,)).start()



            except Exception as e:
                logger.error(e)


    def shutdown(self):
        self.event.set()
        self.client.close()



