from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse,HttpRequest,HttpResponseBadRequest,HttpResponseNotFound
from django.shortcuts import render
import jwt,simplejson
from django.conf import settings
from user.views import auth
from .models import Post,Content
import datetime
from user.models import User
import  math
#post方法

@auth
def pub(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        payload_title = payload['title']
        payload_content = payload['content']
        print(request.user_id,'post/pub!!!!!!')
        print(request.user_name,'post/pub!!!!!!')
        post:Post = Post()
        post.posttitle = payload_title
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        #添加时区
        post.postauthor = User.objects.filter(pk=request.user_id).get()
        # "Post.postauthor" must be a "User" instance.
        # 有外键，必须是一个User实例
        print(post.postauthor)
        post.save()

        content = Content()
        content.post=post
        content.content=payload_content
        content.save()
        return JsonResponse({'id':request.user_id,'username':request.user_name,'title':payload_title}, status=200)
    except Exception as e:
        print(e,'---------+++++++++++++++++++++++++')
        return HttpResponseBadRequest('登录错误！！！')
#zhongsb的cookie
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNCwiZGF0ZXRpbWUiOjE1Nzg5MTY4NDMuNjA5fQ.9G_UQTIEKHNYvU6lj-NX0PQP-um-weDR8aiekMArqf0


#get方法实现
def get(request:HttpRequest,*args): #路径类似 /post/1
    try:
        title_id=int(args[0])   #注意数据类型
        post = Post.objects.get(pk=title_id)
        print(post)
        print('----------------------------')
        if post:
            ret = {
                'post_id':post.id,
                'title':post.posttitle,
                'author':post.postauthor.id,
                'author_id':post.postauthor_id, #也可以写post.postauthor_id,数据库实际生成的字段
                'postdate':post.postdate.timestamp(), #由前端决定以什么样的格式显示
                'content':post.content.content   #一对一关系建立好可以直接调用
            }
            return JsonResponse(ret,status=200)
    except Exception as e:
        print(e)
        return HttpResponseNotFound('Not Found！！！！！！！')

def getall(request:HttpRequest):
    try:   #http://127.0.0.1:8000/post/?page=1  通过查询字符串传参页数
        page = int(request.GET.get('page',None))
        page = page if page>0 else 1
        # 使用GET方法获取查询字符串参数
    except Exception :
        page = 1

    try:  #定义每页条数，通常大部分20条
        size = int(request.GET.get('size',None))
        size = size if size>0 and size<10 else 5
        # 使用GET方法获取查询字符串参数
    except Exception :
        size = 5 #定义每页条数，通常大部分20条

    #分页起点和终点
    start = (page-1)*size  #page=2 size=5  start=6
    end = start+size  #10
    posts = Post.objects.order_by('-postdate').all()[start:end]
    count = Post.objects.order_by('-postdate').all().count()
    #数据库查询使用-取反，使用[]分页,
    # [1,2] 就是第二条，从第1+1条开始，到第2条
    if posts:
        ret = {
            'posts':[
                {
                    'post_id':post.id,
                    'post_title':post.posttitle,
                    'post_date':str(post.postdate)
                }for post in posts
            ],
            'pageinfo':{
                'page':page,
                'size':size,
                'count':count,
                'pages':math.ceil(count/size)
            }
        }
    else:
        return HttpResponseNotFound('无此页面')
    return JsonResponse(ret,status=201)
