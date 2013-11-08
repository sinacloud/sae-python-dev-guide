SAE Python环境
=======================

SAE应用运行于沙箱环境之中，SAE会根据负载在后端的多个节点中选择一个来处理HTTP请求。
SAE Python支持标准WSGI应用。

请求处理
-------------

SAE使用请求的域名来决定处理的应用。比如 `http://your_app_name.sinaapp.com` 的请求会被路由给名为
`your_app_name` 的应用来处理。

每个应用可以同时运行多个版本，版本以数字为标示，默认版本为1。如果需要访问非默认版本，
需要在域名的前面加上版本号作为子域名： `http://version.your_app_name.sinaapp.com` 。
  
默认URL符合以下规则的请求会作为静态文件处理：

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

所有请求的最大执行时间为 `300s` ，超过该时间的请求会被系统强制结束，可能会导致返回502。

对于每个应用的请求，系统会为其维护一个队列，如果出现请求在一定的时间里得不到处理，
服务器会自动给该应用增加instance。如果某一个instance在一段时间里没有任何请求，会被系统回收。

Python环境
-------------------

Python runtime使用的是Python 2.7.3。

* 仅支持运行纯Python的应用，不能动态加载C扩展，即.so，.dll等格式的模块不能使用
* 进程，线程操作受限
* 本地文件系统只读。应用可以读取本应用目录，Python标准库下的内容，如需读写临时文件建议使用StringIO或者cStringIO来替代。

Python默认的模块搜索路径为：当前目录 > 系统目录。添加模块搜索目录的方法为： ::

    import sys
    sys.path.insert(0, your_custom_module_path)

注意：Python当前目录下的子目录只有包含__init__.py才会被Python认为是一个package，
才可以直接import。

用户可以上传和使用 `.pyc` 文件，注意 `.pyc` 文件必须是python2.7.3生成的，否则无效。

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

.. note:: logging默认设置的level是WARNING，也就是level >= WARNING的消息才会被输出。

应用缓存
----------

SAE Python会对应用导入的模块（包括index.wsgi）进行缓存，从而缩短请求响应时间，
对于缓存了的应用，请求处理只是取出index.wsgi中application这个callable并调用。


应用程序配置
-------------

应用程序的配置文件为应用目录下的config.yaml文件。

* 设置使用的worker类型 ::

    worker: tornado | gevent | wsgi

  如果没有设置则默认使用wsgi worker。

  .. warning:: gevent和tornado worker还处在bleeding edge, use at your own risk。

* 使用预装模块

  部分预装的第三方模块不在python的默认模块搜索路径中，需要在config.yaml中配置后才可以使用。 ::

    libraries:
    - name: django
      version: "1.4"

    - name: numpy
      version: "1.6.1"

  name为第三方模块的名称，version为需要使用的版本，这两个字段为必填字段。 :ref:`pre-installed-package-list`

* 静态文件处理 

  ``静态文件夹`` ::

    handlers:
    - url: /static/
      static_path: static
  
  url为URL的前缀，static_path为静态文件所在的目录（相对于应用目录）。

  当请求的url为目录时，服务器会首先尝试static_path下的index.html，当index.html存在时，
  返回index.html的内容，否则返回404。

  ``静态文件``  ::

    handlers:
    - url: /robots.txt
      static_path: robots.txt

    - url: /favicon.ico
      static_path: favicon.ico

* gzip压缩 ::

    handlers:
    - url: /static/
      gzip: on

    - url: /a-big-file.txt
      gzip: on

  url为URL的前缀。

  注意，当客户端支持gzip（HTTP请求的Accept-Encoding中包含gzip）时，服务端才会开启压缩。

.. note::

   1. 部分第三方库已经包含在默认搜索路径中，可以不在config.yaml中指定直接使用。

   2. 如果config.yaml中没有设置静态文件相关的handlers，系统会默认将/static为前缀
      的URL转发到应用目录下的static目录。

   3. 以上两条规则仅为兼容性考虑保留，不推荐使用，请在config.yaml明确配置。

   4. 对于php runtime支持但是python runtime不支持的appconfig，请考虑使用wsgi middleware来完成，参见 :ref:`wsgi_middleware` 

.. _pre-installed-package-list:

预装模块列表
---------------------

    =============================== =================== ====================
    名称                            支持的版本          默认版本
    =============================== =================== ====================
    django                          1.2.7, 1.4, 1.5     1.2.7
    flask                           0.7.2               0.7.2
    flask-sqlalchemy                0.15                0.15
    werkzeug                        0.7.1               0.7.1
    jinja2                          2.6                 2.6
    tornado                         2.1.1, 2.4.1, 3.1.1 2.1.1
    bottle                          0.9.6               0.9.6
    sqlalchemy                      0.7.10              0.7.10
    webpy                           0.36                0.36
    PIL                             1.1.7               1.1.7
    MySQLdb                         1.2.3               1.2.3
    numpy                           1.6.1               无
    lxml                            2.3.4               无
    PyYAML                          3.10                3.10
    misaka                          1.0.2               无
    matplotlib                      1.1.1               无
    PyCrypto                        2.6                 无
    py-bcrypt                       0.2                 无
    greenlet                        0.4.0               0.4.0
    gevent                          1.0rc2              1.0rc2
    markupsafe                      0.15                无
    bitarray                        0.8.0               无
    =============================== =================== ====================

.. note:: 如果模块不存在默认版本或者需要使用非默认版本请在应用配置文件config.yaml中指定。


