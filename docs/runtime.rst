SAE Python环境
=======================

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


命名规范
----------------
SAE Python支持标准WSGI应用

静态目录

* /media
* /static
* /favicon.ico

其他所有请求，都被路由到/index.wsgi:application，即应用根目录index.wsgi文件,
名为application的callable，暂不可修改。

application 使用下列方式创建::

    import sae

    def app(environ, start_response):
        # Your app
        ...

    application = sae.create_wsgi_app(app)


TODO: URL handlers 配置功能


Python限制
-------------------
* 进程，线程操作受限
* 除临时文件，应用自身所在目录外，不可访问本地文件系统


文件系统
--------------
可读: 本app根目录，可以读取本app其他版本的目录

可写: /saetmp/$app_hash/$app_name


代码加载机制
--------------
只有 index.wsgi 被修改，才会触发整个应用的source reloading。现在svn的 post commit hook
并不会自动touch index.wsgi, 临时解决办法是每次提交都手动修改index.wsgi， 比如加减空行。
 

如何调试
------------
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


dev_server 本地开发
--------------------

注意：本工具仅为应用开发便利之用，与真实的sae环境相差较大。

Install
~~~~~~~~~~~~
::

    cd dev_server
    sudo python setup.py install

由于预装模块太多，全部安装太过耗时，故所有依赖关系已在 setup.py 中注掉，
请自行打开你要使用的框架，进行安装。


运行
~~~~~~~~~~
使用svn检出app代码之后，建立以数字为标识的发布目录，切换到发布目录::

    jaime@westeros:~/source/blackfire/1$ pwd
    /home/jaime/source/blackfire/1

建立index.wsgi::

    jaime@westeros:~/source/blackfire/1$ cat index.wsgi
    import sae

    def app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello, world! reloading test3']

    application = sae.create_wsgi_app(app)

运行dev_server.py::

    jaime@westeros:~/source/blackfire/1$ dev_server.py 
    MySQL config not found: app.py
    Start development server on http://localhost:8080/

因为这个简单的应用并没有用到MySQL，所以不需要配置app.py，访问本地
8080端口就可看到Hello, world!


MySQL
~~~~~~~~~~~~

如果你使用sae.core.Application的方式指定数据库信息，可在当前目录
建立一个app.py文件，存放mysql配置信息，示例文件::

    class Application:

        def __init__(self):

            self.mysql_db = ''
            self.mysql_user = ''
            self.mysql_pass = ''
            self.mysql_host = ''
            self.mysql_port = ''

如果你使用的是sae.const常量，则可自行修改。

