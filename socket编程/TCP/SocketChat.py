#多人聊天

import threading
import socket
import datetime
import logging

# logging FORMAT init
FORMAT = '%(asctime)-15s %(process)s %(threadName)s %(message)s'
logging.basicConfig(level=logging.INFO,format=FORMAT)

#多人聊天server
class ChatServer:
    def __init__(self,ip='127.0.0.1',port=9999):
        self.serversocket = socket.socket()
        self.addr = (ip,port)
        self.clients = {}

    def start(self):
        self.serversocket.bind(self.addr)
        self.serversocket.listen()
        logging.info('Start')
        threading.Thread(target=self.accept,name='accept').start()

    def accept(self):
        while True:
            newsock,raddr = self.serversocket.accept()
            self.clients[raddr]=newsock
            logging.info('{},connect'.format(raddr[0]))
            threading.Thread(target=self.recv,args=(newsock,raddr),name='accept-{}'.format(raddr)).start()

    def recv(self,sock:socket.socket,raddr):
        while True:
            data = sock.recv(1024)
            if data.strip() == b'quit' or data.strip() == b'':
                sock.close()
                self.clients.pop(raddr)
                logging.info('{},leave!!!!!!'.format(raddr))
                break
            logging.info(data)
            logging.info('Recv data:{}'.format(data.decode()))
            msg = '{:%Y/%m/%d-%H:%M:%S}\t{} say:{}'.format(datetime.datetime.now(),raddr[0],data.decode())
            for clientsocks in self.clients.values():
                clientsocks.send(msg.encode())

    def stop(self):
        for clientsocks in self.clients.values():
            clientsocks.close()
        self.serversocket.close()

chatserver = ChatServer()
chatserver.start()
while True:
    cmd = input('>>>')
    if cmd == 'quit':
        chatserver.stop()
        break
    print(threading.enumerate())