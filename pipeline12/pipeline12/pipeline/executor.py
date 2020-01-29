from pipeline.model import db, Graph, Vertex, Edge, Pipeline, Track
from pipeline.model import STATE_WAITING, STATE_PENDING, STATE_RUNNING, STATE_FINISH, STATE_FAILED, STATE_SUCCESS
from pipeline.service import transactional
import simplejson

# SELECT * from vertex WHERE vertex.g_id = 1 and vertex.id not in
# (SELECT DISTINCT e.head FROM edge e WHERE e.g_id = 1)

# 使用一个图g_id来创建一个流程放到pipeline，
@transactional()
def start(g_id, name: str, desc: str=None):
    g = db.session.query(Graph).filter(Graph.id == g_id).first()
    if not g:
        raise Exception()

    p = Pipeline()
    p.g_id = g_id
    p.name = name
    if desc: p.desc = desc
    p.state = STATE_RUNNING

    addins = []
    addins.append(p)

    # Track表
    vertexes = db.session.query(Vertex).filter(Vertex.g_id == g_id)
    query = vertexes.filter(Vertex.id.notin_(db.session.query(Edge.head).filter(Edge.g_id == g_id)))
    zeros = {v.id for v in query}

    for v in vertexes:
        t = Track()
        t.pipeline = p
        t.v_id = v.id
        # t.input = v.input
        # t.script = v.script
        t.state = STATE_PENDING if v.id in zeros else STATE_WAITING

        addins.append(t)

    if g.sealed == 0:
        g.sealed = 1
        addins.append(g)

    return addins


@transactional(action='query')
def showpipeline(p_id, stats=[STATE_PENDING], exclude=[STATE_FAILED]): #
    # SELECT track.p_id,pipeline.`name`,pipeline.state,track.id,track.v_id,
    # track.state,    vertex.input,    vertex.script    FROM
    # track    INNER    JOIN    pipeline ON    track.p_id = pipeline.id
    # INNER    JOIN    vertex    ON  track.v_id = vertex.id
    # WHERE    track.p_id = 1
    return db.session.query(
        Track.p_id, Pipeline.name, Pipeline.state,
        Track.id, Track.v_id, Track.state,
        Vertex.input, Vertex.script
    ).join(
        Pipeline, Track.p_id == Pipeline.id
    ).join(
        Vertex, Track.v_id == Vertex.id
    ).filter(Pipeline.state.notin_(exclude))\
    .filter(Track.p_id == 1)\
    .filter(Track.state.in_(stats)).all()


TYPES = {
    'int':int,
    'integer':int,
    'str':str,
    'string':str
}


def finish_params(v_id, d:dict):
    """完成用户提交的参数和不必须参数的统一的验证和处理"""
    data = db.session.query(Vertex.input, Vertex.script).filter(Vertex.id == v_id).first()
    if not data:
        pass # return ?raise

    inp, script = data
    params = {}
    if inp: # ++++++++++++++ 对inp加判断
        inp = simplejson.loads(inp)


        # k ip ; v {"type": "str", "required": true, "default": "192.168.0.100"}
        # {ip: 192.168.0.100}
        for k,v in inp.items():
            typ = TYPES[v.get('type', 'str')]
            if k in d.keys():
                params[k] = typ(d[k])
            else:
                val = v.get('default', None)
                if val:
                    params[k] = typ(v.get('default'))
                else:
                    raise ValueError()
    print('-' * 30)
    print(params)

    return params, script

import re
regex = re.compile(r'{([a-zA-Z\d_]+)}')

# 脚本填充
@transactional()
def finish_script(t_id, params:dict, script:str): #track id == p_id + v_id
    # {"script": "echo \"test1.A\"\nping {ip}", "next": "B"}
    newlines = ''

    script = simplejson.loads(script).get('script', '') # dict

    if script: # echo \"test1.A\"\nping {ip}
        start = 0
        for matcher in regex.finditer(script):
            print(matcher)
            newlines += script[start:matcher.start()]
            key = matcher.group(1)
            value = str(params[key])
            newlines += value
            start = matcher.end()
        else:
            newlines += script[start:]

    print(newlines, '===============')
    t = db.session.query(Track).filter(Track.id == t_id).first()
    if t:
        t.input = simplejson.dumps(params)
        t.script = newlines

    return t

###########################################
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid
import threading
from tempfile import TemporaryFile
from subprocess import Popen
from queue import Queue
from collections import defaultdict


class Executor:
    def __init__(self, workers=5):
        self._executor = ThreadPoolExecutor(max_workers=workers)
        self._tasks = {} # 动态增加future
        self._event = threading.Event()
        self._queue = Queue()

        threading.Thread(target=self._run, args=(2,), name='as_completed').start()
        threading.Thread(target=self._save_track, name='save').start()

    def _execute(self, key, script:str):
        with TemporaryFile('w+') as f:
            # 注意脚本有可能多行
            codes = 0
            code = 1
            for line in script.splitlines():
                proc = Popen(line, shell=True, stdout=f, stderr=f)
                code = proc.wait() # 注意超时
                codes += code
                if code != 0:
                    break
            f.flush()
            f.seek(0)
            txt = f.read() # 注意一点，window执行结果gbk，数据库字段采用默认值utf8
            return key, code, txt


    def submit(self, t_id, script): # 用户提交脚本来执行，但是是异步的
        key = uuid.uuid4().hex
        future = self._executor.submit(self._execute, key, script)  # future
        self._tasks[future] = key, t_id  # k:v

    def _run(self, interval=2):
        while not self._event.wait(interval):
            # 1 fs为空，不进入for
            # 2 不为空，可以进入，开始等待所有fs中的future
            # 3 在future对象一个都没有执行完，as_completed会阻塞
            # 4 一旦future对象done，return、Exception、cancel，for循环会触发一次迭代会拿到future
            # 5 future的result方法是阻塞的方法，阻塞到done为止。如果内部有异常，则把异常抛出，否则返回return的值
            # 6 如果说fs中所有的future都执行了，状态都是done。那么as_completed就不会阻塞，会for持续的遍历
            for future in as_completed(self._tasks):
                print('-' * 30)
                k, t_id = self._tasks[future]
                try:
                    print(100, k, future.done())
                    print('++++++++++++++')
                    print(200, future.result())
                    key, code, txt = future.result()
                    # 包含了code 非0代表script执行失败，此节点任务失败；0表示节点任务成功
                    self._queue.put((key, t_id, code, txt))
                except Exception as e:
                    print(e)
                finally:
                    del self._tasks[future]


    def _save_track(self):
        while not self._event.is_set():
            key, t_id, code, txt = self._queue.get()

            # 入库
            track = db.session.query(Track).filter(Track.id == t_id).one()
            track.output = txt #TODO
            track.state = STATE_SUCCESS if code==0 else STATE_FAILED

            #pipeline
            if code != 0: # 失败流程
                track.pipeline.state = STATE_FAILED

            else:
                # =============== 流转代码 ====================
                # 流转代码， 隐含 自己成功，看别的顶点
                # pipeline是否失败 ， track表中查找是否有失败的
                # 除自己之外
                tracks = db.session.query(Track).filter(
                    Track.p_id == track.p_id).filter(Track.id != track.id)

                states = {STATE_FAILED:0, STATE_SUCCESS:0, STATE_PENDING:0, STATE_RUNNING:0, STATE_WAITING:0}
                count = 0

                for t in tracks:
                    states[t.state] += 1
                    count += 1

                if states[STATE_FAILED] > 0: # 有失败
                    track.pipeline.state = STATE_FAILED
                elif states[STATE_SUCCESS] == count:
                    track.pipeline.state = STATE_FINISH
                else: # 没办法，只能找下一级节点了
                    edges = db.session.query(Edge.tail, Edge.head).filter(Edge.g_id == track.pipeline.g_id)

                    t2h = defaultdict(list) # list
                    h2t = defaultdict(list)

                    for t,h in edges:
                        t2h[t].append(h)
                        h2t[h].append(t)

                    nexts = t2h[track.v_id]
                    #nexts = db.session.query(Edge.tail, Edge.head).filter(Edge.tail == track.v_id).all()
                    if nexts: # 确实有下一级节点
                        for n in nexts:
                            parents = h2t[n] # 父节点的列表
                            # 下一级节点能执行的条件是所有的parents节点的状态应该都是成功的
                            s_count = db.session.query(Track).filter(Track.v_id.in_(parents)).filter(
                                Track.state == STATE_SUCCESS
                            ).count()
                            if len(parents) == s_count:
                                # 其父节点都是成功执行的

                                temp = db.session.query(Track).filter(Track.v_id == n).filter(Track.p_id == track.p_id).one()
                                temp.state = STATE_PENDING

                                db.session.add(temp)
                            else:
                                # 只能在等等了 什么都不做
                                pass

                    else:# 如果没找到下一级节点，这说明你只是其中一个分支的终点，本节点什么都不做
                        pass

            db.session.add(track)
            try:
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()


EXECUTOR = Executor()









