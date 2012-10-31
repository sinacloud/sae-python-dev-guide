Quick Start 快速指引
==============================

Hello, world!
-----------------

首先我们以一个简单的hello world应用介绍一下一个Python应用在SAE上的创建和部署过程。

创建应用
~~~~~~~~~~~~~

登录SAE，进入 `我的首页`_ ，点击 `创建新应用` ，创建一个新的应用helloworld。
开发语言选择python。

.. _我的首页: http://sae.sina.com.cn/?m=myapp&a=create

编辑应用代码
~~~~~~~~~~~~~

SAE采用svn来作为代码部署工具，使用svn客户端检出应用helloworld的代码。 ::

    jaime@westeros:~$ svn co https://svn.sinaapp.com/helloworld

每个应用可以创建多个版本，这些版本可以在线上同时运行，每个版本以数字标示，
其代码对应于svn目录下以其版本号命名的目录。

进入helloworld目录，创建一个目录1作为默认版本，切换到目录1。 ::

    jaime@westeros:~$ cd helloworld
    jaime@westeros:~/helloworld$ mkdir 1
    jaime@westeros:~/helloworld$ cd 1

创建应用配置文件config.yaml，内容如下： ::

    name: helloworld
    version: 1

创建index.wsgi，内容如下：

.. literalinclude:: ../examples/helloworld/1/index.wsgi

SAE上的python应用的入口为 `index.wsgi:application` ，也就是 `index.wsgi` 这个文件中名为
`application` 的callable object。在helloworld应用中，该application为一个wsgi callable object。

部署应用
~~~~~~~~~~~

提交刚刚编辑的代码，就可以完成应用在SAE上的部署。

::

    jaime@westeros:~/helloworld$ svn add 1/
    jaime@westeros:~/helloworld$ svn ci -m "initialize project"


在浏览器中输入 `http://helloworld.sinaapp.com` ，就可以访问刚提交的应用了。

.. note:: 

   svn的仓库地址为：https://svn.sinaapp.com/<your-application-name>，
   用户名和密码为sae的安全邮箱和安全密码。

使用web开发框架
-----------------

Django
~~~~~~~~~~

目前SAE上预置了两个版本的django，1.2.7和1.4，默认的版本为1.2.7，在本示例中我们使用1.4版本。

创建一个新的python应用，检出svn代码到本地目录并切换到应用目录。

创建一个django project：mysite。 ::

    jaime@westeros:~/pythondemo$ django-admin.py startproject mysite
    jaime@westeros:~/pythondemo$ ls mysite
    manage.py  mysite/

重命名该project的根目录名为1，作为该应用的默认版本代码目录。 ::

    jaime@westeros:~/pythondemo$ mv mysite 1

在默认版本目录下创建应用配置文件 `config.yaml` ，在其中添加如下内容： ::

    libraries:
    - name: "django"
      version: "1.4"

创建文件index.wsgi，内容如下 ::
    
    import sae 
    from mysite import wsgi

    application = sae.create_wsgi_app(wsgi.application)

最终目录结构如下 ::

    jaime@westeros:~/pythondemo$ ls 1
    index.wsgi manage.py mysite/ 
    jaime@westeros:~/pythondemo/1$ ls 1/mysite
    __init__.py settings.py  urls.py  views.py

部署代码，访问 `http://<your-application-name>.sinaapp.com` ，就可看到Django的欢迎页面了。

`完整示例`_ （ `django tutorial`_ 中的poll、choice程序）

.. _django tutorial: https://docs.djangoproject.com/en/1.4/intro/tutorial01/
.. _完整示例: https://github.com/SAEPython/saepythondevguide/tree/master/examples/django/1.4

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

web.py
~~~~~~~~

index.wsgi

.. literalinclude:: ../examples/webpy/1/index.wsgi

Tornado
~~~~~~~~~~~

**WSGI模式**

index.wsgi

.. literalinclude:: ../examples/pythondemo/4/index.wsgi

**使用Torando Worker**

config.yaml

.. literalinclude:: ../examples/pythondemo/5/config.yaml

index.wsgi

.. literalinclude:: ../examples/pythondemo/5/index.wsgi

.. note::

   1. tornado worker还处在bleeding edge，use at your own risk。
   2. 在应用出现异常的情况下，SAE可能会返回502错误，请在日志中心中查看详细的错误信息。
   3. 目前仅测试过预安装的tornado-2.1.1，其它版本的tornado可能无法使用。


.. tip:: 
   
   以上所有的示例代码的完整版本都可以在我们的github repo中获得。
   https://github.com/SAEPython/saepythondevguide/tree/master/examples/

