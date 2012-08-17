SAE Python环境
=======================

环境信息
----------

SAE Python应用运行于沙箱环境之中，SAE会根据负载在后端的多个节点中选择一个来处理HTTP请求。
SAE Python支持标准WSGI应用。

命名规范: 

* 应用目录

  SAE上的每个应用可以同时运行多个版本，版本以数字为标示，默认版本为1。
  每个版本对应于应用svn根目录下以其版本号命名的一个目录，称为版本目录，
  应用的代码（index.wsgi等）必须放到版本目录里。

  以应用longtalk为例，这个应用有6个版本： ::
  
        jaime@westeros:~/longtalk$ ls
        1  2  3  4  5  6
        jaime@westeros:~/longtalk/1$ ls
        index.wsgi myapp.py
  
  应用默认版本代码所在的目录，称为应用目录。
  该目录会添加到Python runtime的 sys.path 中。该目录也为应用运行时的当前目录。

  访问指定版本的应用： `http://<version>.<application-name>.sinaapp.com`

  不推荐使用os.getcwd()来获取路径信息，建议使用__file__属性。
  
预装模块列表
---------------------

    =============================== =================== ====================
    名称                            支持的版本          默认版本
    =============================== =================== ====================
    django                          1.2.7, 1.4          1.2.7
    flask                           0.7.2               0.7.2
    flask-sqlalchemy                0.15                0.15
    werkzeug                        0.7.1               0.7.1
    jinja2                          2.6                 2.6
    tornado                         2.1.1               2.1.1
    bottle                          0.9.6               0.9.6
    ulibweb                         0.0.1a7             0.0.1a7
    sqlalchemy                      0.7.3               0.7.3
    webpy                           0.36                0.36
    PIL                             1.1.7               1.1.7
    MySQLdb                         1.2.3               1.2.3
    numpy                           1.6.1               None
    lxml                            2.3.4               None
    =============================== =================== ====================

.. note:: 需要使用非默认版本可以在config.yaml中指定。


请求处理
-------------

默认符合以下规则的请求会作为静态文件处理：

* /static/\*
* /favicon.ico

其他所有请求，都被路由到/index.wsgi:application，即应用根目录index.wsgi文件,
名为application的callable，不可修改。

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

Python runtime使用的是Python 2.7.3。

* 仅支持运行纯Python的应用，不能动态加载C扩展，即.so，.dll等格式的模块不能使用
* 进程，线程操作受限
* 除临时文件，应用自身所在目录外，不可访问本地文件系统。本地文件系统不可写入。

本地文件系统可以读取本应用目录，Python标准库下的内容，不支持写入。
如需读写临时文件建议使用StringIO或者cStringIO来替代。

Python默认的模块搜索路径为：当前目录 > 系统目录。添加模块搜索目录的方法为： ::

    import sys
    sys.path.insert(0, your_custom_module_path)

注意：Python当前目录下的子目录只有包含__init__.py才会被Python认为是一个package，
才可以直接import。

SAE设置了一些自定义的环境变量，这些环境变量可以通过os.environ这个dict获取。 

+ APP_NAME：应用名。
+ APP_VERSION: 当前应用使用的版本号。
+ SERVER_SOFTWARE: 当前server的版本（目前为direwolf/0.1）。
  可以使用这个环境变量来区分本地开发环境还是在线环境，本地开发环境未设置这个值。

日志系统
---------
打印到stdout和stderr的内容会记录到应用的日志中心中，
所以直接使用print语句或者logging模块来记录应用的日志就可以了。

日志内容在 `应用»日志中心» HTTP` 中查看，类别为debug。

应用缓存
----------

SAE Python会对应用导入的模块（包括index.wsgi）进行缓存，从而缩短请求响应时间，
对于缓存了的应用，请求处理只是取出index.wsgi中application这个callable并调用。


应用程序配置
-------------

应用程序的配置文件为应用目录下的config.yaml文件。

* 设置使用的worker类型 ::

    worker: tornado | wsgi

  如果没有设置则默认使用wsgi worker。

* 使用第三方库 ::

    libraries:
    - name: django
      version: "1.4"

    - name: numpy
      version: "1.6.1"

  name为第三方模块的名称，version为需要使用的版本，这两个字段为必填字段。

* 静态文件处理 

  静态文件夹 ::

    handlers:
    - url: /static
      static_dir: static
  
  url为URL的前缀，static_dir为静态文件所在的目录（相对于应用目录）。

.. note::

   1. 部分第三方库已经包含在默认搜索路径中，可以不在config.yaml中指定直接使用。

   2. 如果config.yaml中没有设置静态文件相关的handlers，系统会默认将/static为前缀
      的URL转发到应用目录下的static目录。

   3. 以上两条规则仅为兼容性考虑保留，不推荐使用，请在config.yaml明确配置。
