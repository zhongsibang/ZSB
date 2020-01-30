from flask import Flask, make_response, render_template, jsonify
from .service import getdag

# 创建application
app = Flask('pipeline_web')

@app.route('/', methods=['GET'])
def index(): # 视图函数
    return render_template('index.html')

@app.route('/<int:graphid>')
def showdag(graphid:int):
    return render_template('chart{}.html'.format(graphid))


@app.route('/dag/<int:graphid>') # (rule, **options):
def showajaxdag(graphid):
    if graphid == 1:
        return simplegraph()
    elif graphid == 2:
        return jsonify(getdag(1))
    elif graphid == 3:
        return jsonify(getdag(1))

def simplegraph():
    xs = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    data = [5, 20, 36, 10, 10, 20]
    return jsonify({'xs': xs, 'data': data})



