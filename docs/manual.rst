Quick Start 快速指引
==============================

Hello, world!
------------------
1. 创建新应用

http://sae.sina.com.cn/?m=myapp&a=create

以应用blackfire为例。

2. 检出svn代码

::

    svn co https://svn.sinaapp.com/blackfire

3. 建一个目录1作为默认版本，在此下面新建文件 index.wsgi

::

   jaime@westeros:~/source/apps/blackfire$ mkdir 1
   jaime@westeros:~/source/apps/blackfire$ cd 1
   jaime@westeros:~/source/apps/blackfire/1$ touch index.wsgi
   jaime@westeros:~/source/apps/blackfire/1$ 

index.wsgi

.. literalinclude:: ../examples/blackfire/1/index.wsgi

4. 提交代码

::

    svn commit


5. 访问应用

http://blackfire.sinaapp.com


命名规范
----------------
SAE Python支持标准的WSGI应用

静态目录

* /media
* /static
* /favicon.ico

其他所有请求，都被路由到/index.wsgi:application，即应用根目录index.wsgi文件,
名为application的callable，暂不可修改。

TODO: URL handlers 配置功能


SAE Python的限制
-------------------
* 进程，线程操作受限
* 除临时文件，应用自身所在目录外，不可访问本地文件系统

重新加载代码
~~~~~~~~~~~~~~~
只有 index.wsgi 被修改，才会触发整个应用的source reloading。现在svn的 post commit hook
并不会自动touch index.wsgi, 临时解决办法是每次提交都手动修改index.wsgi， 比如加减空行。
 
调试
~~~~~
复杂程序建议您本地调试成功后，再上传运行。

SAE Python 版本为 2.6.7。如果你使用内置的第三方库版本，请注意使用同样的版本调试，
如支持的Django为1.2.7。

如何捕获wsgi应用的异常，请参阅 http://www.python.org/dev/peps/pep-0333/

501 页面对应的常见处理办法，请检查:

* 模块是否正确安装
* 是否遵循WSGI规范，返回iterator
* 数据库设置是否正确，是否已在SAE管理界面启用MYSQL，是否已创建数据表，初始化
* 是否已经打开framework的debug功能

如果有404错误，试试访问  http://$appname.sinaapp.com/debug 

SAE预装的第三方模块
---------------------
::

    Django-1.2.7.tar.gz
    mitsuhiko-flask-sqlalchemy-0.15-0-g08689c7.zip
    mitsuhiko-werkzeug-0.7.1-0-g22cca39.zip
    mitsuhiko-jinja2-2.6-0-gabfbc18.zip
    Flask-0.7.2.tar.gz
    MySQL-python-1.2.3.tar.gz
    tornado-2.1.1.tar.gz
    bottle-0.9.6.tar.gz
    sinatpy2.x-(2011-6-8).zip


使用Django框架
--------------

NOTE: 目前SAE Python使用的是 *Django-1.2.7* 。

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
   
访问 `http://mysite.sinaapp.com` ，会看到一个 `Welcome to Django`
的页面，It worked!

7. Hello, Django!

在mysite/目录下新建一个views.py，内容如下

.. literalinclude:: ../examples/pythondemo/1/mysite/views.py

修改urls.py，启用admin，打开import admin的注释，新增一条规则用于解析hello::

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


MySQL数据库
~~~~~~~~~~~
   
`mysite/settings.py` 数据库配置::
        
        import sae.core
        app = sae.core.Application()

        DATABASES = {
            'default': {
                'ENGINE': 'mysql',
                'NAME': app.mysql_db,
                'USER': app.mysql_user,
                'PASSWORD': app.mysql_pass,
                'HOST': app.mysql_host,
                'PORT': app.mysql_port,
            }
        }

`sae.core.Application()` 获取app信息，在 `sae.create_wsgi_app` 初始化SAE环境后
调用才起作用。

创建数据表::
    
    django-admin.py sqlall all-installed-app-names > some-file
    
将sql文件导入到SAE线上环境中。

开发可使用本地mysql数据库，在发布时将其导入到SAE线上数据库:

#. 使用mysqldump或者phpMyAdmin等工具从本地数据库导出数据库。
#. 进入SAE后台应用管理>服务管理>MySQL页面，初始化MySQL。
#.  进入管理MySQL页面，选择导入，导入刚才导出的sql文件即可。

http://pythondemo.sinaapp.com/admin/ root:root

http://pythondemo.sinaapp.com/demo/


MySQL数据库静态信息
---------------------
::

    SAE_MYSQL_HOST_M = 'w.rdc.sae.sina.com.cn'
    SAE_MYSQL_HOST_S = 'r.rdc.sae.sina.com.cn'
    SAE_MYSQL_PORT = '3307' # 请根据框架要求自行转换为int
    
    mysql_db = 'app_%s' % app_name
    mysql_user = access_key
    mysql_pass = secret_key

应用的access_key, secret_key，可在应用管理界面的汇总信息中看到。


使用Flask框架
-------------

index.wsgi

.. literalinclude:: ../examples/pythondemo/2/index.wsgi

Hello, world! 和 MySQL, myapp.py 

.. literalinclude:: ../examples/pythondemo/2/myapp.py

http://2.pythondemo.sinaapp.com/demo


使用Bottle框架
--------------

index.wsgi

.. literalinclude:: ../examples/pythondemo/3/index.wsgi

http://3.pythondemo.sinaapp.com


使用Tornado框架
---------------

index.wsgi

.. literalinclude:: ../examples/pythondemo/4/index.wsgi

http://4.pythondemo.sinaapp.com

:doc: bugs.rst

Notes
---------

改变默认版本之后，请确保当前版本路径在sys.path最前面，防止误导入到旧版本的模块

SAE app 代码以数字标识版本，如pythondemo应用有4个版本::

    jaime@westeros:~/source/chenfeng/pythondemo$ ls
    1  2  3  4

代码必须被放到某个版本数字目录里，默认为版本 1

svn使用参考 http://sae.sina.com.cn/?m=devcenter&content_id=215&catId=212


示例代码下载
--------------

http://appstack.sinaapp.com/static/download/sae-python-examples.tar.bz2


意见反馈
----------------

http://sae.sina.com.cn/?m=feedback


