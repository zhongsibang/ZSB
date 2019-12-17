import socket
import threading

class ChatClient:
    def __init__(self,ip='127.0.0.1',port=9999):
        self.sock = socket.socket()
        self.raddr = (ip,port)
        self.event =  threading.Event()

    def start(self):
        self.sock.connect(self.raddr)
        self.sock.send(b'Hello,I am ready')
        threading.Thread(target=self.recv,name='recv').start()

    def send(self,msg:str):
        msg='Client-------{}'.format(msg).encode()
        self.sock.send(msg)

    def recv(self):
        while True:
            data = self.sock.recv(1024)
            print(data.decode())

    def stop(self):
        self.sock.close()

if __name__ == "__main__":
    cc = ChatClient()
    cc.start()
    while True:
        cmd = input('>>>')
        if cmd.strip() == 'quit':

            cc.stop()
            break
        cc.send(cmd.encode())