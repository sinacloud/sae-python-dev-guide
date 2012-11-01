FAQ
===============

BUG反馈以及问题求助
-------------------------

关于SAE Python相关服务的问题可以在以下地方反馈和提问。

* `SAE Python邮件列表`_ （推荐）

  订阅邮件列表
  发送邮件至： sae-python+subscribe@googlegroups.com
  
  退订邮件列表
  发送邮件至： sae-python+unsubscribe@googlegroups.com
  
  发表主题
  发送邮件至： sae-python@googlegroups.com
  
  订阅和退订时发送空邮件即可。如果想修改订阅方式，可以登录Google论坛后在设置中进行更改。


* `SAE Python豆瓣小组（一些旧帖子的存档） <http://www.douban.com/group/pythoncitadel/>`_

关于Python编程的其它问题，推荐到 `CPyUG邮件列表`_ 寻求帮助。

.. _SAE Python邮件列表: http://groups.google.com/group/sae-python
.. _CPyUG邮件列表: http://groups.google.com/group/python-cn?hl=zh-CN

如何调试
------------

复杂程序建议您本地调试成功后，再上传运行。

SAE Python 版本为 2.7.3，本地调试时注意不要使用高于此版本的python。

如果你使用内置的第三方库，本地调试时最好使用同样的版本。

对于50x页面，如果异常被web框架捕获，则需要打开web框架的调试开关，查看详细的异常信息。如果异常被python server捕获，
python server会直接在浏览器中打印出异常。

.. note:: 在header已经发出的情况下，异常在浏览器中可能显示不出来，请查看日志。


没有我要使用的包怎么办
------------------------

对于纯python的package，See :ref:`howto-use-sae-python-with-virtualenv`

对于含有c extension的package，目前SAE还无法直接支持，如果需要这些package，可以申请预装。

`预装申请`_

.. _预装申请: https://github.com/SAEPython/saepythondevguide/issues/new

.. note::

   很多package对package里的c extension都会提供一个python的fallback版本，这类package在sae上也可以
   直接使用，只是速度上相对于使用c extension会稍慢一点。


如何使用新浪微博API
----------------------

+   使用 `weibopy`_

    该模块已经内置，可以直接使用。 完整示例请参考： `examples/weibo`_  。

+   使用 `sinaweibopy`_ (推荐)

    新浪微博API OAuth 2 Python客户端

.. _weibopy: http://code.google.com/p/sinatpy/
.. _examples/weibo: https://github.com/SAEPython/saepythondevguide/tree/master/examples/weibo/1
.. _sinaweibopy: http://open.weibo.com/wiki/SDK#Python_SDK


如何在Cron中使用微博API
------------------------

因为现在weibo api需要提供调用者的ip（合法的公网ip），sae默认提供的是http请求的client的ip，
但是对于cron和taskqueue，由于是sae的内部请求，无法获取公网ip。所以需要用户手工设置一个。
设置方法如下： ::

    import os
    os.environ['REMOTE_ADDR'] = 调用者公网ip

请务必将这段代码放在请求处理代码执行的必经路径上。比如在Flask中：::

    @app.before_request
    def before_request():
        import os
        os.environ['REMOTE_ADDR'] = 调用者公网ip

Django框架下数据库的主从读写
-----------------------------

参见Django官方文档 `Multiple databases`_

.. _Multiple databases: https://docs.djangoproject.com/en/1.2/topics/db/multi-db/#multiple-databases

关于svn的问题 
--------------------------- 

遇到奇怪的SVN错误，可以： 

+ 重新在本地新建目录，检出干净的svn 
+ 或者先保存代码，然后删除该版本，重新导入 

你也许需要新建一个版本，默认版本无法删除。 


MySQL gone away问题
----------------------

MySQL连接超时时间为30s，不是mysql默认的8小时，所以你需要在代码中检查是否超时，是否需要重连。

对于使用sqlalchemy的用户，需要在请求处理结束时调用 `db.session.close()` ，关闭当前session，
将mysql连接还给连接池，并且将连接池的连接recyle时间设的小一点（推荐为10s）。

如何区分本地开发环境和线上环境
-------------------------------------
::

    if 'SERVER_SOFTWARE' in os.environ: 
        # SAE 
    else: 
        # Local 


如何serve django admin app的静态文件
------------------------------------

方法一：

修改 `settings.py` 中的 `STATIC_ROOT` 为 `static/` 。

运行 `python manage.py collectstatic` 将静态文件收集到应用的 `static` 子目录下。

修改 `config.yaml` ，添加对static文件夹下的静态文件的handlers。 ::

    handlers:
    - url: /static
      static_dir: path/to/mysite/static

方法二：

在开发调试（settings.py中debug=True）过程中，可以将 `staticfiles_urlpatterns`_ 加到你的URLConf，让django来处理admin app的静态文件： ::

    urls.py
    --------
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns = patterns('',
        ...

        # Uncomment the next line to enable the admin:
        url(r'^admin/', include(admin.site.urls)),
    )

    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

由于sae默认static为静态文件目录，需要修改config.yaml，添加任意一条规则覆盖默认行为。 ::

    config.yaml
    -----------
    ...

    handlers:
    - url: /foo
      static_dir: foo

ref:

https://docs.djangoproject.com/en/1.4/ref/contrib/staticfiles/
https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/modwsgi/#serving-the-admin-files

.. _staticfiles_urlpatterns: https://docs.djangoproject.com/en/dev/howto/static-files/#staticfiles-development

如何在SAE上使用Uliweb
----------------------

Thanks to limodou#gmail.com

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


