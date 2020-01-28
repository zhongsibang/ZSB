from .cm import ConnectionManage
from .config import MASTER_URL

class Master:
    def __init__(self, url=MASTER_URL):
        self.cm = ConnectionManage(url)

    def start(self):
        self.cm.start()

    def shutdown(self):
        self.cm.shutdown()

