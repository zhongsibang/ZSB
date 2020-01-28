from .cm import ConnectionManage
from .config import *

class Agent:
    def __init__(self, url=MASTER_URL, myidpath=MYID_PATH):
        self.cm = ConnectionManage(url, myidpath)

    def start(self):
        self.cm.start() # 返回吗？阻塞效果

    def shutdown(self):
        self.cm.shutdown()



