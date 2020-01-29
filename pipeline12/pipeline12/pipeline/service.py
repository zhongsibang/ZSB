from .model import Graph, Vertex, Edge
from .model import Pipeline, Track, db
from functools import wraps

def transactional(action='add'): # del, query
    def _transactional(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            ret = fn(*args, **kwargs)
            try:
                if action == 'add':
                    if isinstance(ret, (list, tuple)):
                        for o in ret:
                            db.session.add(o)
                        ret = ret[0]
                    else:
                        db.session.add(ret)
                db.session.commit()
                return ret
            except Exception as e:
                db.session.rollback()
                raise e

        return wrapper
    return _transactional


@transactional()
def create_graph(name:str, desc:str=None):
    g = Graph()
    g.name = name
    if desc: g.desc = desc

    return g

@transactional()
def add_vertex(g:Graph, name:str, inp:str=None, script:str=None):
    v = Vertex()
    v.name = name
    if script: v.script = script
    if inp: v.input = inp
    v.g_id = g.id

    return v

@transactional()
def add_edge(g:Graph, tail:Vertex, head:Vertex):
    e = Edge()
    e.tail = tail.id
    e.head = head.id
    e.g_id = g.id

    return e


# 一个示例，其他删除请自行解决
# 删除一个顶点
@transactional(action='del')
def del_vertex(v_id):

    v = db.session.query(Vertex).filter(Vertex.id == v_id).first() # all list ; first list[0]
    if v:
        g_id = v.g_id

        sealed = db.session.query(Graph.sealed).filter(Graph.id == g_id).first() # list[0] None
        if sealed: # 判断列表有没有元素
            sealed = sealed[0]
            if sealed == 0: # 没有封闭
                pass
            else:
                raise Exception()
        else:
            raise ValueError()

        edges = db.session.query(Edge).filter((Edge.tail == v_id) | (Edge.head == v_id)).delete()
        v.delete()





# # kahn 算法实现1
# def check_graph1(g:Graph) -> bool:
#     # 获取所有顶点列表
#     lst = db.session.query(Vertex).filter(Vertex.g_id == g.id).all() # list
#     if not lst:
#         return False
#     vertexes = [v.id for v in lst] # 顶点id的列表
#
#     edges = db.session.query(Edge.tail, Edge.head).filter(Edge.g_id == g.id).all() # 所有边
#
#     print(vertexes)
#     print(edges)
#     print('-' * 30)
#
#     # [1, 2, 3, 4]
#     # [(1, 2), (1, 3), (3, 2), (2, 4)]
#     while True:
#         for i, v in enumerate(vertexes): # 至少有一个
#             del_vertex_index = None
#             for _,h in edges:
#                 if h == v:
#                     # 如果找到head是v，说明它有入库，直接跳过测试下一个顶点
#                     break
#             else: # 无break，1 edges是空 2 没有找到 都是入度为0的
#                 del_vertex_index = i
#                 # 删除所有关联到此顶点的边 们
#                 del_edge_indexes = []
#                 for j, (t,_) in enumerate(edges):
#                     if t == v:
#                         del_edge_indexes.append(j)
#                 for index in reversed(del_edge_indexes):
#                     del edges[index]
#                 # 说明找到了该删除的顶点和其边们
#                 break
#         else:
#             # 这些顶点有入度
#             return False
#
#         del vertexes[del_vertex_index]
#         if len(edges) + len(vertexes) == 0: #?
#             return True

from collections import defaultdict

# kahn 算法实现2

def check_graph(g:Graph) -> bool:
    # 获取所有顶点列表
    lst = db.session.query(Vertex).filter(Vertex.g_id == g.id).all() # list
    if not lst:
        return False
    vertexes = {v.id for v in lst} # 顶点集


    query = db.session.query(Edge).filter(Edge.g_id == g.id) # 所有边
    # 如何写?
    # {1, 2, 3, 4}
    # defaultdict(<class 'list'>, {1: [(1, 2), (1, 3)], 3: [(3, 2)], 2: [(2, 4)]})
    # 字典，tail、head为key
    edges = defaultdict(list)
    heads = set()
    for e in query:
        edges[e.tail].append((e.tail, e.head))
        heads.add(e.head)

    print(vertexes)
    print(edges)
    print(heads)
    print('-' * 30)

    if len(edges):
        # 有顶点也有边的情况
        # 入度为0
        zeros = vertexes - heads # 差集就是入度为0的顶点们

        if len(zeros) == 0:
            return False

        # 找到了，怎么办，马上删
        for z in zeros: # v_id
            if z in edges.keys():
                del edges[z]

        while edges:
            vertexes = heads
            heads = set()

            for k, edgelist in edges.items():
                for e1,e2 in edgelist :
                    heads.add(e2)

            zeros = vertexes - heads # heads = vertexes - zeros

            if len(zeros) == 0: #
                return False

            # 找到了，怎么办，马上删
            for z in zeros:  # v_id
                if z in edges.keys():
                    del edges[z]

    # 可以写数据库的graph表了 checked = 1
    graph = db.session.query(Graph).filter(Graph.id == g.id).first()
    if graph:
        graph.checked = 1
        db.session.add(graph)
        try:
            db.session.commit()
            return  True
        except Exception as e:
            db.session.rollback()
            raise e
    else:
        return False



















