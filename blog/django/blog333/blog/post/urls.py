from django.urls import include, path,re_path
from .views import get,getall,pub

urlpatterns = [
    re_path(r'^pub/', pub),
    re_path(r'^(\d+)$', get),
    re_path(r'^$',getall)
    #django2.2.9和3 写法不同，3中如果使用正则表达式需要使用re_path
]