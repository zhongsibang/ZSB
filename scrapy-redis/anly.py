#分析
import redis
import json
import jieba

words = {}
stopwords=set()
totle = 0
with open('f:/temp/chineseStopWords.txt',encoding='gbk') as f:
    for line in f:
        stopwords.add(line.rstrip('\r\n'))

rdb = redis.Redis('192.168.0.200',db=0)
print(rdb.lrange('review:items',0,-1))
comments = rdb.lrange('review:items',0,-1)
for comment in comments:     #提取词汇
    rev = json.loads(comment).get('comment')
    for  word in jieba.cut(rev):
        if word not in stopwords:  #不在停用词范围的菜统计
            words[word] = words.get(word,0)+1
            totle+=1
print(words)
print(sorted(words.items(),key=lambda x:x[1],reverse=True))
#分割关键词，倒序，

#可视化,词云
frenq = {word:count/totle for word,count in words.items()}
print(frenq)
from wordcloud import WordCloud
import matplotlib.pyplot as plt

w = WordCloud(font_path='simhei.ttf',max_font_size=40,scale=15) #size最大字体大小，scale清晰度
w.fit_words(frenq) #使用单词和词频创建词云
plt.figure(2)
plt.axis("off")  #不打印坐标系
plt.imshow(w, interpolation="bilinear") #图显示在二位坐标轴上
plt.show()
# # lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()

# plt.axis("off")

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
# d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
#
# # Read the whole text.
# text = open(path.join(d, 'constitution.txt')).read()
#
# # Generate a word cloud image
# wordcloud = WordCloud().generate(text)
#
# # Display the generated image:
# # the matplotlib way:
# import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
#
# # lower max_font_size
# wordcloud = WordCloud(max_font_size=40).generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()


# jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
# strs=["我来到北京清华大学","乒乓球拍卖完了","中国科学技术大学"]
# for str in strs:
#     seg_list = jieba.cut(str,use_paddle=True) # 使用paddle模式
#     # print("Paddle Mode: " + '/'.join(list(seg_list)))
#     print(list(seg_list))
# #
# # seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# # print("Full Mode: " + "/ ".join(seg_list))  # 全模式
# #
# # seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# # print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
# #
# # seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# # print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))