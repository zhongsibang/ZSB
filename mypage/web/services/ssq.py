from datasource.getfromfile import SSQ_DATA
from web.config import *
from flask import redirect,url_for

def ssq_show_page(page):
    ssqdata, pages = SSQ_DATA
    context = {'res':[]}
    start = SSQ_SHOW_SIZE*(page-1) #0,0-14
    end = start + SSQ_SHOW_SIZE if (start + SSQ_SHOW_SIZE)<=len(ssqdata) else len(ssqdata)-1#15
    for i in range(start,end):
        context['res'].append(ssqdata[i])
    startpage = page//5*5+1 if page%5!=0 else (page//5-1)*5+1
    endpage = startpage+5-1 if startpage+5-1<pages else pages
    context['pageinfo']=[startpage,endpage]
    context['currentpage']=page
    return context

def ssq_fenxi_blue(items=5):
    ssqdata,_ = SSQ_DATA
    fenxidata = sorted(ssqdata[0:items],reverse=False)
    dates = []
    blues = []
    for x in fenxidata:
        dates.append(x[0])
        blues.append(x[7])
    return (dates,blues)
    # print(dates,blues,'---------------------------')
