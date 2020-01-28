from common.state import *


class Task:
    """任务封装类，任务就是类的一个个实例"""
    def __init__(self, id, script, timeout,
                 targets, pararrel=1,
                 fail_count=0, fail_rate=0):
        self.id = id
        self.script = script # 任务，shell脚本
        self.timeout = timeout
        #################
        self.parallel = pararrel  # 最大并发
        self.fail_count = fail_count
        self.fail_rate = fail_rate

        self.targets = targets # 此任务派发给几个agent执行['id1', 'id2']
        self.state = WAITING

    def __repr__(self):
        return '<Task {}>'.format(self.id)





