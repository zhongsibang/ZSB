import zerorpc
from .message import Message


class ConnectionManage:
    def __init__(self, url):
        self.server = zerorpc.Server(Message())
        self.url = url

    def start(self):
        self.server.bind(self.url)
        self.server.run()

    def shutdown(self):
        self.server.close()






