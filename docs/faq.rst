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

如何使用virtualenv管理依赖关系
-------------------------------

当你的应用依赖很多第三方包时，可以使用virtualenv来管理并导出这些依赖包，
流程如下：

首先，创建一个全新的Python虚拟环境目录ENV，启动虚拟环境。 ::

    $ virtualenv --no-site-packages ENV
    $ source ENV/bin/activate
    (ENV)$

可以看到命令行提示符的前面多了一个(ENV)的前缀，现在我们已经在一个全新的虚拟环境中了。

使用pip安装应用所依赖的包并导出依赖关系到requirements.txt。 ::

    (ENV)$ pip install Flask Flask-Cache Flask-SQLAlchemy 
    (ENV)$ pip freeze > requirements.txt

编辑requirements.txt文件，删除一些sae内置的模块，eg. flask, jinja2, wtforms。

使用dev_server/bundle_local.py工具，
将所有requirements.txt中列出的包导出到本地目录virtualenv.bundle目录中。
如果文件比较多的话，推荐压缩后再上传。 ::

    (ENV)$ bundle_local.py -r requirements.txt
    (ENV)$ cd virtualenv.bundle/
    (ENV)$ zip -r ../virtualenv.bundle.zip .

将virutalenv.bundle目录或者virtualenv.bundle.zip拷贝到应用的目录下。

修改index.wsgi文件，在导入其它模块之前，将virtualenv.bundle目录或者
virtualenv.bundle.zip添加到module的搜索路径中，示例代码如下： ::

    import os
    import sys

    app_root = os.path.dirname(__file__)

    # 两者取其一
    sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle'))
    sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))

到此，所有的依赖包已经导出并加入到应用的目录里了。

更多virtualenv的使用可以参考其官方文档。 http://pypi.python.org/pypi/virtualenv

.. note::

   1. 请删除requirements.txt中的wsgiref==0.1.2这个依赖关系，否则可能导致
      bundle_local.py导出依赖包失败。

   2. 有些包是not-zip-safe的，可能不工作，有待验证。 含有c扩展的package
      不能工作。

