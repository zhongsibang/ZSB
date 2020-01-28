import uuid
import os.path
import socket
import datetime
import netifaces
import ipaddress
from .config import MYID_PATH

class Message:
    def __init__(self, myidpath:str=MYID_PATH):
        # 从文件中读取，一个agent一个唯一id，一旦生成不可改变，除非删除myid文件
        self.id = ''
        # 文件是否存在
        if os.path.exists(myidpath):
            with open(myidpath, encoding='utf-8') as f:
                id = f.readline().strip()
                if len(id) == 32:
                    self.id = id

        if not self.id:
            with open(myidpath, 'w', encoding='utf-8') as f:
                self.id = uuid.uuid4().hex
                f.write(self.id)

    def _get_addresses(self):
        ips = []

        for iface in netifaces.interfaces():
            x = netifaces.ifaddresses(iface)
            ipv4s = x.get(2, [])
            for ipv4 in ipv4s:
                ip = ipv4['addr']

                ip = ipaddress.ip_address(ip)
                if ip.version != 4:
                    continue
                if ip.is_multicast:
                    continue
                if ip.is_reserved:
                    continue
                if ip.is_link_local:
                    continue
                if ip.is_loopback:
                    continue
                if str(ip) == '0.0.0.0':
                    continue

                ips.append(str(ip))

        return ips

    def reg(self):
        return {
            'id':self.id,
            'hostname':socket.gethostname(),
            'timestamp':datetime.datetime.now().timestamp(),
            'ips':self._get_addresses()
        }

    def heartbeat(self):
        return {
            'id': self.id,
            'hostname': socket.gethostname(),
            'timestamp': datetime.datetime.now().timestamp(),
            'ips': self._get_addresses()
        }

    def result(self, task_id, code, output):
        return {
            'id': self.id, # myid, agent'id
            'task_id': task_id,
            'code':code,
            'output':output
        }















