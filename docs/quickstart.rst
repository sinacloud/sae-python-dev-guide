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
    config.yaml index.wsgi manage.py mysite/ 
    jaime@westeros:~/pythondemo/1$ ls 1/mysite
    __init__.py settings.py  urls.py  views.py

部署代码，访问 `http://<your-application-name>.sinaapp.com` ，就可看到Django的欢迎页面了。

`完整示例`_ （ `django tutorial`_ 中的poll、choice程序）

.. _django tutorial: https://docs.djangoproject.com/en/1.4/intro/tutorial01/
.. _完整示例: https://github.com/sinacloud/sae-python-dev-guide/tree/master/examples/django/1.4

`django-1.2.7示例`_

.. _django-1.2.7示例: https://github.com/sinacloud/sae-python-dev-guide/tree/master/examples/django/1.2.7


处理用户上传文件
``````````````````

在setttings.py中添加以下配置。 ::

    # 修改上传时文件在内存中可以存放的最大size为10m
    FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

    # sae的本地文件系统是只读的，修改django的file storage backend为Storage
    DEFAULT_FILE_STORAGE = 'sae.ext.django.storage.backend.Storage'
    # 使用media这个bucket
    STORAGE_BUCKET_NAME = 'media'
    # ref: https://docs.djangoproject.com/en/dev/topics/files/

发送邮件
``````````

在settings.py中添加以下配置，即可使用sae的mail服务来处理django的邮件发送了。 ::

    ADMINS = (
        ('administrator', 'administrator@gmail.com'),
    )

    # ref: https://docs.djangoproject.com/en/dev/ref/settings/#email
    EMAIL_BACKEND = 'sae.ext.django.mail.backend.EmailBackend'
    EMAIL_HOST = 'smtp.example.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'sender@gmail.com'
    EMAIL_HOST_PASSWORD = 'password'
    EMAIL_USE_TLS = True
    SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

数据库的主从读写
``````````````````

参见Django官方文档 `Multiple databases`_

.. _Multiple databases: https://docs.djangoproject.com/en/1.2/topics/db/multi-db/#multiple-databases

如何syncdb到线上数据库
````````````````````````

如下配置数据库，即可执行 `python manage.py syncdb` 直接syncdb到线上数据库。 ::

    # 线上数据库的配置
    MYSQL_HOST = 'w.rdc.sae.sina.com.cn'
    MYSQL_PORT = '3307'
    MYSQL_USER = 'ACCESSKEY'
    MYSQL_PASS = 'SECRETKEY'
    MYSQL_DB   = 'app_APP_NAME'

    from sae._restful_mysql import monkey
    monkey.patch()

    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.mysql',
            'NAME':     MYSQL_DB,
            'USER':     MYSQL_USER,
            'PASSWORD': MYSQL_PASS,
            'HOST':     MYSQL_HOST,
            'PORT':     MYSQL_PORT,
        }
    }

.. warning:: 本feature还在开发中，目前还很buggy。

如何serve admin app的静态文件
``````````````````````````````

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

Flask
~~~~~~~~~~

index.wsgi

.. literalinclude:: ../examples/flask/index.wsgi

myapp.py 

.. literalinclude:: ../examples/flask/myapp.py


Bottle
~~~~~~~~~~

index.wsgi

.. literalinclude:: ../examples/bottle/index.wsgi

web.py
~~~~~~~~

index.wsgi

.. literalinclude:: ../examples/webpy/index.wsgi

Tornado
~~~~~~~~~~~

**WSGI模式**

index.wsgi

.. literalinclude:: ../examples/tornado/wsgi/index.wsgi

**使用Torando Worker**

config.yaml

.. literalinclude:: ../examples/tornado/async/config.yaml

index.wsgi

.. literalinclude:: ../examples/tornado/async/index.wsgi

.. note::

   1. tornado worker还处在bleeding edge，use at your own risk。
   2. 在应用出现异常的情况下，SAE可能会返回502错误，请在日志中心中查看详细的错误信息。
   3. 目前仅测试过预安装的tornado-2.1.1，其它版本的tornado可能无法使用。
   4. 对于tornado worker，如果需要使用非预装的tornado，请务必将tornado模块放在应用根目录下（index.wsgi所在的目录）。


.. tip:: 
   
   以上所有的示例代码的完整版本都可以在我们的github repo中获得。
   https://github.com/sinacloud/sae-python-dev-guide/tree/master/examples/

