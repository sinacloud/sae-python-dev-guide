dev_server
===========================

注意：本工具仅为应用开发便利之用，与真实的sae环境相差较大。

Install
--------------
::

    cd dev_server
    sudo python setup.py install

框架的依赖关系在 setup.py 中已注掉，故默认不安装任何框架，请自行安装。


使用
------------
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
-----------

在应用发布目录下建立app.py文件，存放app的配置信息，可复制本目录下
的示例文件::

    class Application:

        def __init__(self):

            self.mysql_db = ''
            self.mysql_user = ''
            self.mysql_pass = ''
            self.mysql_host = ''
            self.mysql_port = ''

此时，使用app = sae.core.Application(); app.mysql_db.. 的代码就可在
本地工作。当然，你也可以不使用这种方式，直接指定MySQL数据库的连接信息。

