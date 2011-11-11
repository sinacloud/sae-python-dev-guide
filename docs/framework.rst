Web开发框架
================

Django
--------------

NOTE: 目前SAE Python使用的版本是 *Django-1.2.7* , 请确保你安装的是这个版本。

1. 建立一个新的Python应用mysite
   
2. 检出SVN代码到本地目录

3. 新建文件index.wsgi，内容如下
    
.. literalinclude:: ../examples/pythondemo/1/index.wsgi

4. 初始化django应用
   
::

   django-admin.py startproject mysite
   
5. 从django安装目录复制admin 的media目录
   
::
   
   cp -rf django/contrib/admin/media/ .

去除.svn 目录::

   find . -type d -name ".svn"|xargs rm -rf

目录结构如下::

    jaime@westeros:~/source/chenfeng/pythondemo/1$ ls
    index.wsgi  media  mysite  README
    jaime@westeros:~/source/chenfeng/pythondemo/1$ ls media/
    css  img  js
    jaime@westeros:~/source/chenfeng/pythondemo/1$ ls mysite/
    demo  __init__.py  manage.py  settings.py  urls.py  views.py
    jaime@westeros:~/source/chenfeng/pythondemo/1$ 

6. 提交代码
   
访问 `http://mysite.sinaapp.com` ，就可看到Django的欢迎页面了。

7. Hello, Django!

在mysite/目录下新建一个views.py，内容如下

.. literalinclude:: ../examples/pythondemo/1/mysite/views.py

修改urls.py，新增一条规则解析hello，同时打开admin的注释::

    # Uncomment the next two lines to enable the admin:
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        ...
        (r'^$', 'mysite.views.hello),
        (r'^admin/', include(admin.site.urls)),
    )


在setttings.py中开启admin组件::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        ...
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',
    )


提交代码，访问 `http://mysite.sinaapp.com/` 

Django 数据库配置见 MySQL 节。


Flask
-------------

index.wsgi

.. literalinclude:: ../examples/pythondemo/2/index.wsgi

myapp.py 

.. literalinclude:: ../examples/pythondemo/2/myapp.py

http://2.pythondemo.sinaapp.com/demo


Bottle
--------------

index.wsgi

.. literalinclude:: ../examples/pythondemo/3/index.wsgi

http://3.pythondemo.sinaapp.com


Tornado
---------------

index.wsgi

.. literalinclude:: ../examples/pythondemo/4/index.wsgi

http://4.pythondemo.sinaapp.com

