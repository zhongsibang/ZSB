
from distutils.core import setup
import glob

setup(name='blog',
      version='1.0',
      description='blog project',
      author='zsb',
      author_email='zsb@zsb.com',
      url='http://zsb.com',
      packages=['blog', 'post','user','user.templatetags'],
      #写包名,如果不需要用代码创建数据库，就不用迁移migrations
      py_modules = ['manage'],
      #可以不打包manage.py
      data_files = ['requirements'] + glob.glob('templates/*.html') #获取目录下匹配的文件包括
      #data_files = ['templates/index.html','templates/cheng99.html']
     )


