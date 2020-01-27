"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.http import HttpRequest,HttpResponse,JsonResponse
from django.shortcuts import render
import datetime
from user import views as user_views
#官网推荐写法
from django.urls import include, path


def index(request:HttpRequest):
    contex = {
        'a':100,
        'b':0,
        'c':list(range(10,20)),
        'd':'abc',
        'date':datetime.datetime.now()
    }
    return render(request,'index.html',context=contex,status=200)

def cheng99(request:HttpRequest):
    contex ={ 'data':['{}*{}={}'.format(i,j,i*j)for i in range(1,10) for j in range(1,10)]}
    return render(request,'cheng99.html',context=contex,status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$',index),
    re_path(r'^index/',index),
    re_path(r'^cheng99',cheng99),
    path('user/', include('user.urls')),
    path('post/', include('post.urls'))
    #django2.2.9和3 写法不同，3中如果使用正则表达式需要使用re_path
]
