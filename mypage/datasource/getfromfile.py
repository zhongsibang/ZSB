from datasource import SOURCEFILE
import csv
from web.config import SSQ_SHOW_SIZE

def getnumbs(sourcefile:str):
    ret = []
    with open(sourcefile, encoding='utf8') as f:
        lines = csv.reader(f)
        for line in lines:
            if line:
                numbs = ''.join(line).split(',')
                date, r1, r2, r3, r4, r5, r6, b = tuple(numbs)
                ret.append((int(date),int(r1),int(r2),int(r3),int(r4),int(r5),int(r6),int(b)))
    ret = sorted(ret,key=lambda x: x[0],reverse=True)
    if len(ret)%SSQ_SHOW_SIZE == 0:
        pages = int(len(ret)//SSQ_SHOW_SIZE)
    else:
        pages = int(len(ret)//SSQ_SHOW_SIZE+1)
    return (ret,pages)

SSQ_DATA = getnumbs(SOURCEFILE)
# print(SSQ_DATA)
    # dates = []
    # r1s = []
    # r2s = []
    # r3s = []
    # r4s = []
    # r5s = []
    # r6s = []
    # bs = []
    # for items in ret:
    #     dates.append(items[0])
    #     r1s.append(items[1])
    #     r2s.append(items[2])
    #     r3s.append(items[3])
    #     r4s.append(items[4])
    #     r5s.append(items[5])
    #     r6s.append(items[6])
    #     bs.append(items[7])
    # print('************************************************')
    # print(sum(r1s)/len(r1s))
    # print(sum(r2s)/len(r2s))
    # print(sum(r3s)/len(r3s))
    # print(sum(r4s)/len(r4s))
    # print(sum(r5s)/len(r5s))
    # print(sum(r6s)/len(r6s))
    # print(sum(bs)/len(bs))
    # print('*******************************************************')
