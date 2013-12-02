相关工具
==============

代码部署
------------

SAE Python使用SVN作为部署工具。使用SVN部署代码到SAE需要遵循以下规则：

    SVN根目录下只允许存在以正整数命名的目录，不允许有文件存在，
    这些目录为应用的版本目录，每个版本目录下才可以放应用对应版本的代码。

以应用longtalk为例，这个应用有6个版本： ::
  
        jaime@westeros:~/longtalk$ ls
        1  2  3  4  5  6
        jaime@westeros:~/longtalk/1$ ls
        index.wsgi myapp.py

SVN限制： 

- 文件名或目录名不允许含有以下字符：",*,?,<,>,|，另外文件或文件名的开始与结束也不允许有空格。
- 上传单个文件大小不超过20M
- 单个目录下的文 件个数不能超过2000个
- 每个应用代码总大小不超过100M
- 单个版本代码总大小不超过50M

.. warning::
   
   1. 不要使用svn cp，mv，目前还不支持这两个操作。
   2. 建议使用命令行工具中的saecloud deploy命令来部署代码。

本地开发环境
--------------

本地开发环境仅为应用开发便利之用，对sae python环境的模拟并不完全。

安装
~~~~~~~~~

直接使用 `pip` 或者 `easy_install` 安装 `sae-python-dev` 包即可。

或者可以选择从github下载源码安装。

::

    $ git clone https://github.com/sinacloud/sae-python-dev-guide.git
    $ cd sae-python-dev-guide/dev_server
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

.. note::

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


命令行工具saecloud
--------------------

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

.. note::

   `deploy` 和 `export` 命令需要用到svn，请先安装svn命令行工具。
   windows用户可以在这里下载：http://sourceforge.net/projects/win32svn/

.. _howto-use-saecloud-install:

安装依赖的第三方包
~~~~~~~~~~~~~~~~~~

在应用目录中执行下面的命令安装依赖的第三方包。 ::

    saecloud install package [package ... ]

如果应用的依赖关系比较多，也可以这些依赖关系写到依赖文件中，例如： ::

    Framework==0.9.4
    Library>=0.2

假设上面的依赖文件的文件名为requirements.txt，你可以执行下面的命令安装所有的依赖包。 ::

    saecloud install -r requirements.txt

该命令会安装依赖包到应用目录下名为 `site-packages` 的目录里。如果文件比较多的话，推荐压缩site-packages目录。 ::

    cd site-packages/
    zip -r ../site-packages.zip .

修改index.wsgi文件，在导入其它模块之前，将 `site-packages` 目录或者 `site-packages.zip` 
添加到module的搜索路径中。 ::

    import os
    import sys

    root = os.path.dirname(__file__)

    # 两者取其一
    sys.path.insert(0, os.path.join(root, 'site-packages'))
    sys.path.insert(0, os.path.join(root, 'site-packages.zip'))

这样就可以在应用中使用这些依赖包了。

.. tip::

   安装指定版本的package：saecloud install package==version

.. _cloudsql.py:

cloudsql.py
-------------

cloudsql.py是SAE MySQL服务的一个命令行客户端，用户可以使用cloudsql.py来直接操作应用的线上数据库。 ::

    alan@sina:~/python$ cloudsql.py -u ACCESSKEY -p SECRETKEY APP_NAME
    SAE MySQL Client

    Type "help" or "?" for help.

    Connecting to Cloud SQL database "app_shellpy" on host w.rdc.sae.sina.com.cn.
    Using readline for history management.
    Loading history file "/home/alan/.saecloud/app_shellpy.hist"
    mysql>

如果想要在代码中直接操作线上的数据库，在 `import MySQLdb`  （并不一定要安装MySQLdb包）之前执行以下的代码即可： ::

    # 只在本地开发环境中执行
    import os
    if 'SERVER_SOFTWARE' not in os.environ:
        from sae._restful_mysql import monkey
        monkey.patch()

可用插件
--------------

SAE Python Shell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SAE Python Shell是一个wsgi中间件，提供了一个在线的interactive shell，便于在线调
试app，查看系统信息等。（由 shellpy_ 修改而来)。

.. _shellpy: http://code.google.com/p/google-app-engine-samples/source/browse/trunk/shell/shell.py


..  py:class:: ShellMiddleware(app, password=None)
    :module: sae.ext.shell

    app: 你的应用callable

    password: 可选，登录shell时需要输入的口令，用于保护shell不被非法访问。


使用步骤:

- 该插件需要使用 `memcache` 服务，请事先开启。

- 修改index.wsgi，启用shell插件，示例如下::

    import sae
    from sae.ext.shell import ShellMiddleware

    def app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ["Hello, world!"]

    application = sae.create_wsgi_app(ShellMiddleware(app))

- 访问地址 https://<your-app-name>.sinaapp.com/_sae/shell ，根据提示输入你设置的口令

- 或者你也可以在命令行下面使用 `saecloud shell <your-app-name> [-p PASSWORD]` 来访问在线shell。 ::

    alan@sina:~/shellpy$ saecloud shell pylabs -proot
    Python 2.7.3 (default, Mar 27 2013, 18:11:21) 
    [GCC 4.4.6 20120305 (Red Hat 4.4.6-4)]
    Type "help", "copyright", "credits" or "license" for more information.

    >>> 

..  warning::

    测试期间请谨慎使用，建议不使用时从源码中注释掉此shell。
