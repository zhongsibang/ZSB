from .model import db, Pipeline, Track, Vertex, Edge
import random

def randomxy():
    return random.randint(300, 500) # 随机模仿 x y坐标

def getdag(p_id): # 根据pipeline的id返回流程数据，让前端页面绘制DAG图
    ps = db.session.query(
        Pipeline.id, Pipeline.name, Pipeline.state,
        Vertex.id, Vertex.name, Vertex.script, Track.script
    ).join(Track, (Pipeline.id == Track.p_id) & (Pipeline.id == 1))\
    .join(Vertex, Vertex.id == Track.v_id)

    edges = db.session.query(Edge.tail, Edge.head).\
        join(Pipeline, (Pipeline.g_id == Edge.g_id) & (Pipeline.id == 1))


    data = [] # 顶点数据
    vertexes = {} # 让edges查询少join
    title = ''
    for p_id, p_name, p_state, v_id, v_name, v_script, t_script in ps:
        if not title:
            title = p_name
        data.append({
            'name': v_name,
            'x': randomxy(),
            'y': randomxy(),
            'value': t_script if t_script else v_script
        })
        vertexes[v_id] = v_name
    print(data)

    links = [] # 边
    for tail, head in edges:
        links.append({
            'source' : vertexes[tail],
            'target' : vertexes[head]
        })

    return {'title':title, 'data':data, 'links':links}







