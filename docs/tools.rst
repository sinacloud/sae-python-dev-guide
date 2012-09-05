相关工具
==============

本地开发环境
--------------

目前支持的服务包括：mysql, taskqueue, memcache, storage, mail。
本地开发环境仅为应用开发便利之用，对sae python环境的模拟并不完整。

安装
~~~~~~~~~

::

    $ git clone http://github.com/SAEPython/saepythondevguide.git
    $ python setup.py install

基本使用
~~~~~~~~~~

进入应用的本地开发目录，也就是index.wsgi和config.yaml所在的目录。运行如下的命令启动测试server： ::

    $ dev_server.py 
    MySQL config not found: app.py
    Start development server on http://localhost:8080/

访问 http://localhost:8080 端口就可以访问你的应用了。

使用MySQL服务
~~~~~~~~~~~~~~

首先配置好MySQL本地开发server。然后使用 `--mysql` 参数运行dev_server.py。 ::

    $ dev_server.py --mysql=user:password@host:port

现在你可以在应用代码中像在SAE线上环境一样使用MySQL服务了。
dev_server.py默认使用名为 `app_应用名` 的数据库。

使用storage服务
~~~~~~~~~~~~~~~~

使用 `--storage-path` 参数运行dev_server.py。 ::

    $ dev_server.py --storage-path=/path/to/local/storage/data

本地的storage服务使用以下的目录结构来模拟线上的storage。 ::

    storage-path/
          domain1/
                key1
                key2
          domain2/
          domain3/

--storage-path配置的路径下每个子文件夹会映射为storage中的一个domain，
而每个子文件夹下的文件映射为domain下的一个key，其内容为对应key的数据。

.. note: 

    为方便调试，dev_server自带的sae.storage在某个domain不存在的情况下会自动创建该domain。
    线上环境中的domain需要在sae后台面板中手动创建。

使用pylibmc
~~~~~~~~~~~~~

dev_server自带了一个dummy pylibmc，所以无须安装pylibmc就可以直接使用memcache服务了。
该模块将所有的数据存贮在内存中，dev_server.py进程结束时，所有的数据都会丢失。

使用kvdb
~~~~~~~~~~~~~

kvdb默认数据存在内存中，dev_server.py进程结束时，数据会全部丢失，如果需要保存数据，
请使用如下命令行启动dev_server.py。 ::

    $ dev_server.py --kvdb-file=/path/to/kvdb/local/file


.. _howto-use-sae-python-with-virtualenv:

使用virtualenv管理依赖关系
----------------------------

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

saecloud
----------------------

saecloud是一个简单的命令行部署工具。它分离了代码部署和代码托管，使你可以选择习惯使用的vcs工具，同时还能够快速部署本地app目录到SAE服务器上。

部署代码
~~~~~~~~~~

进入应用目录（也就是config.yaml和index.wsgi所在的目录）。  ::

    $ cat config.yaml 
    name: memorystone
    version: 2
    $ saecloud deploy

saecloud从config.yaml文件获得信息，判断将要把代码部署到哪个应用的哪个版本。上面的命令会将应用部署到memorystone的版本2上。
saecloud deploy命令接受一个可选参数: app代码所在路径，默认为当前目录'.'。

.. note::

   1. 删除应用版本目前仍然只能在前端管理界面中操作。
   2. 如果代码量较大，则上传时间较慢，请耐心等待
   3. 不推荐混合使用saecloud deploy和svn，虽然saecloud deploy部署之前会自动更新代码，但是如果有代码冲突则会导致本地状态不一致。解决办法为删除本地cache目录： `rm -rf ~/.saecloud`

导出应用代码
~~~~~~~~~~~~~~

导出memorystone应用版本2到本地目录： ::

    $ saecloud export memorystone 2 --username fooxxx@gmail.com --password barxxx
    Exporting to memorystone

第一个参数为应用名字，第二个参数为版本，可选，默认为版本1。 第一次使用时，请指定你的代码访问帐号信息：username 安全邮箱, password。之后的命令不用在输入此信息。

上传文件到storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

对于无法在storage管理页面上传的大文件，可以使用saecloud提供的命令行工具来上传。 ::

    saecloud upload-data app-name domain file [file ...]

可用插件
--------------

SAE Python Shell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SAE Python Shell是一个wsgi中间件，提供了一个在线的interactive shell，便于在线调
试app，查看系统信息等。（由 shellpy_ 修改而来)。

.. _shellpy: http://code.google.com/p/google-app-engine-samples/source/browse/trunk/shell/shell.py


..  py:class:: ShellMiddleware(app, secret_code)
    :module: sae.ext.shell

    app: 你的应用callable

    secret_code: 登录shell时需要输入的口令，用于保护shell不被非法访问。如本例的口令为 hugoxxxx，你可以设置你自己的口令，长度应不小于8个字节


使用步骤:

- 该插件需要使用 sae.kvdb_ 服务，请事先开启。

.. _sae.kvdb: http://appstack.sinaapp.com/static/doc/release/testing/service.html#id9

- 修改index.wsgi，启用shell插件，示例如下::

    import sae
    from sae.ext.shell import ShellMiddleware

    def app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ["Hello, world!"]

    application = sae.create_wsgi_app(ShellMiddleware(app, 'hugoxxxx'))

- 访问地址 https://$yourappname.sinaapp.com/_web/shell ，根据提示输入你设置的口令

..  warning::

    请使用https方式访问shell地址 /_web/shell，这样可以加密传输口令。测试期间请谨慎使用，建议不使用时从源码中注释掉此shell。
