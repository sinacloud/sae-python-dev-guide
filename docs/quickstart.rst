Quick Start 快速指引
==============================

Hello, world!
-----------------

创建新应用
~~~~~~~~~~~

登录SAE，进入 `我的首页`_ ，点击 `创建新应用` ，创建一个新的应用helloworld。

.. _我的首页: http://sae.sina.com.cn/?m=myapp&a=create

检出svn代码
~~~~~~~~~~~~~

执行下面的命令创建应用目录并检出svn代码。 ::

   jaime@westeros:~$ svn co https://svn.sinaapp.com/helloworld

创建index.wsgi
~~~~~~~~~~~~~~~~~

创建一个目录1作为默认版本，在此下面新建文件 `index.wsgi` 。 ::

   jaime@westeros:~$ cd helloworld
   jaime@westeros:~/helloworld$ mkdir 1
   jaime@westeros:~/helloworld$ cd 1
   jaime@westeros:~/helloworld/1$ touch index.wsgi

编辑index.wsgi，内容如下：

.. literalinclude:: ../examples/blackfire/1/index.wsgi

提交代码
~~~~~~~~~~~~

::

   jaime@westeros:~/helloworld$ svn add 1/
   jaime@westeros:~/helloworld$ svn ci -m "initialize project"


访问应用
~~~~~~~~~~~~~~

在浏览器中输入 `http://helloworld.sinaapp.com` ，就可以访问刚提交的应用了。

.. note:: 

   svn的仓库地址为：http://svn.sinaapp.com/<your-application-name>，
   用户名和密码为sae的安全邮箱和安全密码。


使用web开发框架
-----------------

Django
~~~~~~~~~~

目前SAE Python使用的版本是 *Django-1.2.7* , 请确保你安装的是这个版本。

#. 建立一个新的Python应用，检出svn代码到本地目录，建立默认版本目录1并切换到此目录。

#. 新建文件index.wsgi，内容如下
    
   .. literalinclude:: ../examples/pythondemo/1/index.wsgi

#. 初始化django应用::

    django-admin.py startproject mysite
   
   最终目录结构如下::

    jaime@westeros:~/pythondemo/1$ ls
    index.wsgi  media  mysite  README
    jaime@westeros:~/pythondemo/1$ ls media/
    css  img  js
    jaime@westeros:~/pythondemo/1$ ls mysite/
    demo  __init__.py  manage.py  settings.py  urls.py  views.py

#. 提交代码
   
   访问 `http://<your-application-name>.sinaapp.com` ，就可看到Django的欢迎页面了。

#. Hello, Django!

   在mysite/目录下新建一个views.py，内容如下

   .. literalinclude:: ../examples/pythondemo/1/mysite/views.py

   修改urls.py，新增一条规则解析hello。 ::

        # Uncomment the next two lines to enable the admin:
        # from django.contrib import admin
        # admin.autodiscover()

        urlpatterns = patterns('',
            ...
            (r'^$', 'mysite.views.hello),
            #(r'^admin/', include(admin.site.urls)),
        )

   提交代码，访问 `http://<your-application-name>.sinaapp.com/` ，ok，熟悉的Hello，World!出现了。

因为django的WSGI Handler不会处理静态文件请求（静态文件是由manage.py来处理的），如果你需要使用django的admin模块，
你需要从django安装目录复制admin 的media目录到应用目录下的/media目录中。 ::

    cp -rf django/contrib/admin/media/ <your-application-home>/media

如果你定义了自己的templates目录，admin应用的模板可能无法使用，需要将admin的系统模块添加到settings.py中::
   
    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
    +   '/usr/local/sae/python/lib/python2.6/site-packages/django/contrib/admin/templates/admin',
        os.path.join(PROJ_DIR, 'templates'),
    )

FIXME: admin模块和自定义模块关系

Flask
~~~~~~~~~~

index.wsgi

.. literalinclude:: ../examples/pythondemo/2/index.wsgi

myapp.py 

.. literalinclude:: ../examples/pythondemo/2/myapp.py


Bottle
~~~~~~~~~~

index.wsgi

.. literalinclude:: ../examples/pythondemo/3/index.wsgi


Tornado
~~~~~~~~~~~

index.wsgi

.. literalinclude:: ../examples/pythondemo/4/index.wsgi


Uliweb
~~~~~~~~~~~

Thanks to limodou At gmail.com

uliweb的安装
+++++++++++++

为搭建本地开发环境，你需要安装uliweb 0.0.1a7以上版本或svn中的版本， 简单的安装可以是::

    easy_install Uliweb
    
安装后在Python环境下就可以使用uliweb命令行工具了。

目前Uliweb支持Python 2.6和2.7版本。3.X还不支持。

Hello, Uliweb
+++++++++++++++++

让我们从最简单的Hello, Uliweb的开发开始。首先假设你已经有了sae的帐号.

#. 创建一个新的应用，并且选择Python环境。
#. 从svn环境中checkout一个本地目录
#. 进入命令行，切換到svn目录下
#. 创建Uliweb项目::

    uliweb makeproject project
    
   会在当前目录下创建一个 ``project`` 的目录。这个目录可以是其它名字，不过它是和后面要使用的 ``index.wsgi`` 对应的，所以建议不要修改。
    
#. 创建 ``index.wsgi`` 文件，Uliweb提供了一个命令来做这事::

    uliweb support sae
    
   这样会在当前目录下创建一个 ``index.wsgi`` 的文件和 ``lib`` 目录。注意执行时是在svn的目录，即project的父目录中。 

   ``index.wsgi`` 的内容是::

    import sae
    import sys, os
    
    path = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.join(path, 'project')
    sys.path.insert(0, project_path)
    sys.path.insert(0, os.path.join(path, 'lib'))
    
    from uliweb.manage import make_application
    app = make_application(project_dir=project_path)
    
    application = sae.create_wsgi_app(app)
    
   其中 ``project`` 和 ``lib`` 都已经加入到 ``sys.path`` 中了。所以建议使用上面
   的路径，不然就要手工修改这个文件了。

#. 然后就可以按正常的开发app的流程来创建app并写代码了，如::

    cd project
    uliweb makeapp simple_todo
    
    这时一个最简单的Hello, Uliweb已经开发完毕了。
    
#. 如果有静态文件，则需要放在版本目录下，Uliweb提供了命令可以提取安装的app的静态文件::

    cd project
    uliweb exportstatic ../static

#. 如果有第三方源码包同时要上传到sae中怎么办，Uliweb提供了export命令可以导出已经
   安装的app或指定的模块的源码到指定目录下::

    cd project
    uliweb export -d ../lib #这样是导出全部安装的app
    uliweb export -d ../lib module1 module2 #这样是导出指定的模块
    
   为什么还需要导出安装的app，因为有些app不是放在uliweb.contrib中的，比如第三方
   的，所以需要导出后上传。但是因为export有可能导出已经内置于uliweb中的app，所以
   通常你可能还需要在 ``lib`` 目录下手工删除一些不需要的模块。

#. 提交代码
   
   访问 ``http://<你的应用名称>.sinaapp.com`` ，就可看到项目的页面了。

数据库配置
+++++++++++++++++

Uliweb中内置了一个对sae支持的app，还在不断完善中，目前可以方便使用sae提供的MySql
数据库。

然后修改 ``project/apps/settings.ini`` 在 ``GLOBAL/INSTALLED_APPS`` 最后添加::

    [GLOBAL]
    INSTALLED_APPS = [
    ...
    'uliweb.contrib.sae'
    ]
    
然后为了支持每个请求建立数据库连接的方式，还需要添加一个Middleware在settings.ini中::

    [MIDDLEWARES]
    transaction = 'uliweb.orm.middle_transaction.TransactionMiddle'
    db_connection = 'uliweb.contrib.sae.middle_sae_orm.DBConnectionMiddle'

其中第一行是事务支持的Middleware你也可以选择使用。    
    
这样就配置好了。而相关的数据库表的创建维护因为sae不能使用命令行，所以要按sae的
文档说明通过phpMyAdmin来导入。以后Uliweb会増加相应的维护页面来做这事。


web.py
~~~~~~~~

index.wsgi

.. literalinclude:: ../examples/webpy/1/index.wsgi


.. tip:: 
   
   以上所有的示例代码的完整版本可以在我们的github repo中获得。

   https://github.com/SAEPython/saepythondevguide/tree/master/examples/

