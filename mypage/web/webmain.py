from flask import Flask,render_template,url_for,request,redirect,json
from web.config import *
from datasource.getfromfile import SSQ_DATA
from urllib.parse import parse_qs
from web.services.ssq import ssq_show_page,ssq_fenxi_blue

app = Flask(__name__)

@app.route('/',methods=['GET'])
def indexhandler():
    return render_template('index.html')

@app.route('/show/',methods=['GET'])
def ssq_show(page=1):
    ssqdata, pages = SSQ_DATA
    try:
        q_string = request.query_string.decode()
        page = int(parse_qs(q_string).get('page')[0])
    except:
        page = 1
    if page<=0:
        return redirect(url_for('ssq_show',page=1))
    if page>pages:
        return redirect(url_for('ssq_show',page=pages))
    context = ssq_show_page(page)
    return render_template('ssq_show.html',context=context)

@app.route('/fenxi',methods=['GET'])
def ssq_fenxi():
    dates,blues=ssq_fenxi_blue(30)
    return render_template('fenxi.html',dates=dates,blues=blues)

if __name__ == '__main__':
    app.run(IP,PORT,debug=DEBUG)