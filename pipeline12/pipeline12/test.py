import json
from pipeline.service import Graph, Vertex, db
from pipeline.service import create_graph, add_vertex, add_edge
import simplejson

# 测试数据
# 由于将script格式更改了，所以重新提供该函数
# 测试数据
def test_create_dag():
    try:
        # 创建DAG
        g = create_graph('test1') # 成功则返回一个Graph对象
        # 增加顶点
        input = {
            "ip":{
                "type":"str",
                "required":True,
                "default":'127.0.0.1'
            }
        }

        script = {
            'script':'echo "test1.A"\nping {ip}',
            'next':'B'
        }
        # 这里为了让用户方便，next可以接收2种类型，数字表示顶点的id，字符串表示同一个DAG中该名称的节点，不能重复
        a = add_vertex(g, 'A', json.dumps(input), json.dumps(script)) # next顶点验证可以在定义时，也可以在使用时
        b = add_vertex(g, 'B', None, '{"script":"echo B"}')
        c = add_vertex(g, 'C', None, '{"script":"echo C"}')
        d = add_vertex(g, 'D', None, '{"script":"echo D"}')
        # 增加边
        ab = add_edge(g, a, b)
        ac = add_edge(g, a, c)
        cb = add_edge(g, c, b)
        bd = add_edge(g, b, d)

        # 创建环路
        g = create_graph('test2') # 环路
        # 增加顶点
        a = add_vertex(g, 'A', None, '{"script":"echo A"}')
        b = add_vertex(g, 'B', None, '{"script":"echo B"}')
        c = add_vertex(g, 'C', None, '{"script":"echo C"}')
        d = add_vertex(g, 'D', None, '{"script":"echo D"}')
        # 增加边, abc之间的环
        ba = add_edge(g, b, a)
        ac = add_edge(g, a, c)
        cb = add_edge(g, c, b)
        bd = add_edge(g, b, d)

        # 创建DAG
        g = create_graph('test3') # 多个终点
        # 增加顶点
        a = add_vertex(g, 'A', None, '{"script":"echo A"}')
        b = add_vertex(g, 'B', None, '{"script":"echo B"}')
        c = add_vertex(g, 'C', None, '{"script":"echo C"}')
        d = add_vertex(g, 'D', None, '{"script":"echo D"}')
        # 增加边
        ba = add_edge(g, b, a)
        ac = add_edge(g, a, c)
        bc = add_edge(g, b, c)
        bd = add_edge(g, b, d)

        # 创建DAG
        g = create_graph('test4') # 多入口
        # 增加顶点
        a = add_vertex(g, 'A', None, '{"script":"echo A"}')
        b = add_vertex(g, 'B', None, '{"script":"echo B"}')
        c = add_vertex(g, 'C', None, '{"script":"echo C"}')
        d = add_vertex(g, 'D', None, '{"script":"echo D"}')
        # 增加边
        ab = add_edge(g, a, b)
        ac = add_edge(g, a, c)
        cb = add_edge(g, c, b)
        db = add_edge(g, d, b)
    except Exception as e:
        print(e)

from pipeline.service import check_graph
from pipeline.executor import start
from pipeline.executor import showpipeline, finish_params, finish_script, EXECUTOR

# db.drop_all()
# db.create_all()
# test_create_dag()
# print(check_graph(Graph(id=1)))
# print(check_graph(Graph(id=2)))
# print(check_graph(Graph(id=3)))
# print(check_graph(Graph(id=4)))
# start(1, '流程1', '这是第一个图的第一个流程，将封闭此图')




ps = showpipeline(1)
print(ps)

# SELECT track.p_id,pipeline.`name`,pipeline.state,track.id,track.v_id,
# track.state,    vertex.input,    vertex.script    FROM
# track    INNER    JOIN    pipeline ON    track.p_id = pipeline.id
# INNER    JOIN    vertex    ON  track.v_id = vertex.id
# WHERE    track.p_id = 1
for p_id, p_name, p_state, t_id, v_id, t_state, v_input, v_script in ps:
    print(p_id, p_name, p_state, t_id, v_id, t_state, v_input, v_script)
    # 拿 track表中当前指定的p_id Job，它的所有流程节点信息，状态时Pending，排除了pipeline状态时失败的
    # {"ip": {"type": "str", "required": true, "default": "192.168.0.100"}}
    d = {}
    print(v_input, type(v_input), '~~~~~~~~~~~~~~~~') # ++++++ input加判断
    if v_input:
        inp = simplejson.loads(v_input) # => dict

        # 只完成用户的交互，这个往往是在浏览器端完成

        for k,v in inp.items(): # k ip ; v {"type": "str", "required": true, "default": "192.168.0.100"}
            required = v.get('required', False)
            if required: # true
                val = input('{} = '.format(k))
                d[k] = val

    print(d) # 只收集用户提交的参数，不验证

    params, script = finish_params(v_id, d)
    track = finish_script(t_id, params, script)
    print('===============')
    print(track)

    EXECUTOR.submit(track.id, track.script)










