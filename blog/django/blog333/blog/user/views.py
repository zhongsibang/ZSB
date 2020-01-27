from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse,HttpRequest,HttpResponseBadRequest
import simplejson
from .models import User
from django.conf import settings
import jwt,bcrypt
import datetime
from functools import wraps

from django.db.models import Q

def gen_token(user_id):
    secretkey = settings.SECRET_KEY  # 获取获取setting中的SECRET_KEY
    return jwt.encode({'user_id':user_id,'datetime':datetime.datetime.now().timestamp()},secretkey,'HS256').decode()

# 身份验证装饰器
AUTH_EXPIRE = 8*60*60
def auth(fn):
    # @wraps(fn)
    def wrapper(request:HttpRequest):
        token = request.META.get('HTTP_JWT',None) #从头信息中获取jwt tokne
        secretkey = settings.SECRET_KEY
        try:
            payload = jwt.decode(token,secretkey,['HS256'])
            user_id  = payload.get('user_id',None)
            user_name = User.objects.filter(pk=user_id).get().username
            #需要补充用户是否存在、是否已被禁用
            #需要验证jwt是否过期，过期处理，是重新登录还是续期
            current = datetime.datetime.now()
            print(payload,'{} 登录成功！！！！！！！！'.format(fn.__name__))
            request.user_id=user_id   #验证成功为request动态增加user_id属性，方便后面函数使用
            request.user_name=user_name
            return fn(request)
        except Exception as e:
            print(e,'登录失败111111111111111111111111111')
            return HttpResponseBadRequest('token错误')
    return wrapper

#注册用户
def reg(request:HttpRequest):
    try:
        isdelete = False
        b = simplejson.loads(request.body)
        print(b,type(b))
        username = b['username']
        password = bcrypt.hashpw(b['password'].encode(),bcrypt.gensalt()).decode() #得到密码后加密
        mail = b['mail']
        query = User.objects.filter(mail=mail)
        if query.first():
            return HttpResponseBadRequest('邮箱重复')
        print(query,'^^^^^^^^^^^^^^^',type(query))
        #delete=
        print(username,mail,password)
        user_to_update = User()
        user_to_update.username = username
        user_to_update.mail = mail
        user_to_update.password = password
        user_to_update.isdelete = isdelete

        try:
            user_to_update.save()
            #会自动commit
            res = JsonResponse({
                'id': user_to_update.id,
                'username': user_to_update.username,
                'mail': user_to_update.mail,
                'token': gen_token(user_to_update.id)
            }, status=200)
            return res
        except Exception as e:
            raise

    except Exception as e:
        print(e)
        return HttpResponseBadRequest('参数错误')

#@auth #show = auth(show) = wrapper，GET方法
def show(request:HttpRequest):
    query = User.objects.all()
    ret = {}
    for x in query:
        ret[x.id]=x.username
    print('show!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    ret = JsonResponse(ret,status=200)
    ret["Access-Control-Allow-Origin"]="*"
    return  ret

#登录函数,Post方法
def login(request:HttpRequest):
    try:
        b = simplejson.loads(request.body)
        mail = b['mail']
        password = b['password'].encode()
        checkuser = User.objects.filter(mail=mail).first()
        if checkuser:
            if bcrypt.checkpw(password,checkuser.password.encode()):
                token = gen_token(checkuser.id)
                res = JsonResponse({
                    'id':checkuser.id,
                    'username':checkuser.username,
                    'mail':checkuser.mail,
                    'token':token
                },status=200)
                res.set_cookie('jwt',token) #设置 JWT cookie
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNH0.U1zvJIJuoFTvU6OVa9IJCR3a4bEtrXlaBvjIlSvax8s
                print('login成功！！！！！！！！！！！！！！！！！！！！！！！！')
                print(request.body,'login!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                return res
            else:
                return HttpResponseBadRequest('1登录失败')
        else:
            return HttpResponseBadRequest('2登录失败')
    except Exception as e:
        print(e)
        return HttpResponseBadRequest('3登录失败')


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print(request,'++++++++++++++++++++++++')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response





