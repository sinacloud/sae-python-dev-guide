SAE Python环境
=======================

环境信息
----------

SAE Python运行于沙箱环境之中，

命名规范: 

* 应用目录
  
    应用默认版本代码所在的目录，即index.wsgi所在目录，如 /data1/www/htdocs/115/longtalk/1。
    该目录会添加到Python runtime的 sys.path 中。该目录也为应用运行时的当前目录。

    不推荐使用os.getcwd()来获取路径信息，建议使用__file__属性。

* 应用版本目录

    你可同时运行多个版本的app，每个版本以数字为标识，如 `~/source/app/longtalk` 为app longtalk的根目录，下面有6个版本::

        jaime@westeros:~/source/app/longtalk$ ls
        1  2  3  4  5  6

    应用代码必须放到版本目录里::

        jaime@westeros:~/source/app/longtalk$ cd 1
        jaime@westeros:~/source/app/longtalk/1$ ls
        dispatcher.py  index.wsgi  myapp.py


预装模块列表
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
    Uliweb-0.0.1a7.zip
    SQLAlchemy-0.7.3.tar.gz
    web.py-0.36.tar.gz
    setuptools-0.6c11/pkg_resources.py
    pylibmc-1.2.2.tar.gz
    Flask-WTF-0.5.2.tar.gz
    WTForms-0.6.3.zip
    Imaging-1.1.7.tar.gz


请求处理
-------------

SAE Python支持标准WSGI应用，

静态目录

* /media
* /static
* /favicon.ico

其他所有请求，都被路由到/index.wsgi:application，即应用根目录index.wsgi文件,
名为application的callable，暂不可修改。

application 使用下列方式创建

.. module:: sae
.. function:: create_wsgi_app(app)

   将标准wsgi应用封装为适宜在SAE上运行的应用

::

    import sae

    def app(environ, start_response):
        # Your app
        ...

    application = sae.create_wsgi_app(app)


Python环境
-------------------

Python runtime使用的是Python 2.6.7。

* 仅支持运行纯Python的应用，不能动态加载C扩展，即.so，.dll等格式的模块不能使用
* 进程，线程操作受限
* 除临时文件，应用自身所在目录外，不可访问本地文件系统。本地文件系统不可写入。

本地文件系统可以读取本应用目录，Python标准库下的内容，不支持写入。
如需读写临时文件建议使用StringIO或者cStringIO来替代。

日志系统
---------
打印到stdout和stderr的内容会记录到应用的日志中心中，
所以直接使用print语句或者logging模块来记录应用的日志就可以了。

日志内容在 `应用»日志中心» HTTP` 中查看，类别为debug。

应用缓存
----------

SAE Python会对应用导入的模块（包括index.wsgi）进行缓存，从而缩短请求响应时间，
对于缓存了的应用，请求处理只是取出index.wsgi中application这个callable并调用。

如何调试
------------
复杂程序建议您本地调试成功后，再上传运行。

SAE Python 版本为 2.6.7。如果你使用内置的第三方库版本，请注意使用同样的版本调试，
如支持的Django为1.2.7。

如何捕获wsgi应用的异常，请参阅 http://www.python.org/dev/peps/pep-0333/

501 页面对应的常见处理办法，请检查:

* 使用dev_server查看是否有语法错误
* 模块是否正确安装
* 是否遵循WSGI规范，返回iterator
* 数据库设置是否正确，是否已在SAE管理界面启用MYSQL，是否已创建数据表，初始化
* 是否已经打开framework的debug功能

有的framework默认关闭了debug功能，如果程序有问题则只返回500 internal error，没有异常堆栈信息，
这样调试起来很困难。在开发过程中，请确认框架的debug功能处于开启状态。

对于无法加载index.wsgi，index.wsgi中没有application callable等等严重错误，SAE Python会直接在浏览器中打印出异常，
其余应用没有捕获的异常会打印到应用的日志中，如果需要SAE Python将所有应用未捕获的异常打印到浏览器，请按如下创建application。

::

    application = sae.create_wsgi_app(app, debug=True)

.. note:: 在header已经发出的情况下，异常在浏览器中可能显示不出来，请查看日志。

