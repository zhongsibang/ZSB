from django.urls import include, path,re_path
from user import views as user_views
from django.conf import urls

urlpatterns = [
    path('reg/', user_views.reg),
    re_path(r'^show/', user_views.show),
    re_path(r'^login/',user_views.login)
    #django2.2.9和3 写法不同，3中如果使用正则表达式需要使用re_path
]
