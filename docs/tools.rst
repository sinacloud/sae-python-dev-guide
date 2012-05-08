相关工具
==============

使用dev_server进行调试
-------------------------

目前支持的服务包括：mysql, taskqueue, memcache, storage, mail。
大部分的服务直接运行dev_server.py进行调试就可以了，部分服务需要做一些配置。

注意： 本工具仅为应用开发便利之用，对sae python环境的模拟并不完整。

Install
~~~~~~~~~

::

    $ git clone http://github.com/SAEPython/saepythondevguide.git
    $ sudo python setup.py install

基本使用
~~~~~~~~~~

使用svn检出app代码之后，建立以数字为标识的发布目录，切换到发布目录: ::

    $ pwd
    /home/jaime/source/blackfire/1

编辑index.wsgi和config.yaml： ::

    $ vi index.wsgi
    import sae

    def app(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ['Hello, world! reloading test3']

    application = sae.create_wsgi_app(app)

    $ vi config.yaml
    ---
    name: blackfire
    version: 1
    ...

运行dev_server.py。 ::

    $ dev_server.py 
    MySQL config not found: app.py
    Start development server on http://localhost:8080/

访问 http://localhost:8080 端口就可以看到Hello, world!了。

使用MySQL服务
~~~~~~~~~~~~~~

配置好MySQL本地开发server，使用 `--mysql` 参数运行dev_server.py。 ::

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
-------------------------------------------

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
    (ENV)$ zip -r ../virtualenv.bundle.zip。

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

使用saecloud部署应用
-----------------------------------

saecloud是一个简单的命令行部署工具。它分离了代码部署和代码托管，使你可以选择习惯使用的vcs工具，同时还能够快速部署本地app目录到SAE服务器上。

使用svn的代码目录结构::

    jaime@westeros:~/source/app/memorystone$ ls 
    1  2
    jaime@westeros:~/source/app/memorystone$ ls 1
    index.wsgi
    jaime@westeros:~/source/app/memorystone$ ls 2
    index.wsgi
    jaime@westeros:~/source/app/memorystone$ ls -a

该app根目录下面有两个子目录，分别对应于两个app版本，颇为麻烦。

使用saecloud deploy::

    jaime@westeros:~/source/app/memorystone$ ls
    index.wsgi
    jaime@westeros:~/source/app/memorystone$

不再需要数字格式的版本目录了。


安装
~~~~~~

 ::

    jaime@westeros:~/saepythondevguide/dev_server$ sudo python setup.py install
    [sudo] password for jaime: 
    running install
    ....
    jaime@westeros:~/saepythondevguide/dev_server$ saecloud version
    SAE command line v0.0.1
    jaime@westeros:~/saepythondevguide/dev_server$ 

导出已有应用代码
~~~~~~~~~~~~~~~~~~~~~~

帮助信息::

    jaime@westeros:~/source/app$ saecloud 
    usage: saecloud [-h] {version,export,deploy} ...

    positional arguments:
      {version,export,deploy}
                            sub commands
        export              export source code to local directory
        deploy              deploy source directory to SAE
        version             show version info

    optional arguments:
      -h, --help            show this help message and exit
    jaime@westeros:~/source/app$ 

导出memorystone应用版本2到本地目录::

    jaime@westeros:~/source/app$ saecloud export memorystone 2 --username fooxxx@gmail.com --password barxxx
    Exporting to memorystone
    jaime@westeros:~/source/app$ cd memorystone
    jaime@westeros:~/source/app/memorystone$ ls
    index.wsgi
    jaime@westeros:~/source/app/memorystone$

第一个参数为应用名字，第二个参数为版本，可选，默认为版本1。

第一次使用时，请指定你的代码访问帐号信息：username 安全邮箱, password。之后的命令不用在输入此信息。


部署新代码
~~~~~~~~~~~~~~~~~~~

新建config.yaml::

    jaime@westeros:~/source/app/memorystone$ vi config.yaml
    jaime@westeros:~/source/app/memorystone$ cat config.yaml 
    name: memorystone
    version: 2
    jaime@westeros:~/source/app/memorystone$ ls
    config.yaml  index.wsgi

saecloud从config.yaml文件获得信息，判断将要把代码部署到哪个应用的哪个版本。

修改一下index.wsgi，然后运行 saecloud deploy::

    jaime@westeros:~/source/app/memorystone$ saecloud deploy 
    Deploying http://2.memorystone.sinaapp.com
    Updating cache
    Finding changes
    Pushing to server...  done
    jaime@westeros:~/source/app/memorystone$ 

That's it.

saecloud deploy命令接受一个可选参数: app代码所在路径，默认为当前目录'.'。
--username, --password同export命令。

修改一下config.yaml，部署到一个新版本3::

    jaime@westeros:~/source/app/memorystone$ vi config.yaml 
    jaime@westeros:~/source/app/memorystone$ saecloud deploy 
    Deploying http://3.memorystone.sinaapp.com
    Updating cache
    Finding changes
    Pushing to server...  done
    jaime@westeros:~/source/app/memorystone$ cat config.yaml 
    name: memorystone
    version: 3
    jaime@westeros:~/source/app/memorystone$ 


注意:

- 删除应用版本目前仍然只能在前端管理界面中操作。

.. warning::

    cron中的配置 schedule: \*/5 * * * * 目前无法识别，会报语法错误

saecloud和git workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    jaime@westeros:~/source/app$ rm -rf memorystone
    jaime@westeros:~/source/app$ saecloud export memorystone 2
    Exporting to memorystone
    jaime@westeros:~/source/app$ cd memorystone
    jaime@westeros:~/source/app/memorystone$ ls
    config.yaml  index.wsgi
    jaime@westeros:~/source/app/memorystone$ git init
    Initialized empty Git repository in /home/jaime/source/app/memorystone/.git/
    jaime@westeros:~/source/app/memorystone$ git add .
    jaime@westeros:~/source/app/memorystone$ git ci -am "Testing saecloud"
    [master (root-commit) fe7131e] Testing saecloud
     2 files changed, 11 insertions(+), 0 deletions(-)
     create mode 100644 config.yaml
     create mode 100644 index.wsgi
    jaime@westeros:~/source/app/memorystone$ git branch
    * master


    jaime@westeros:~/source/app/memorystone$ git co -b v3
    Switched to a new branch 'v3'
    jaime@westeros:~/source/app/memorystone$ git branch
      master
    * v3
    jaime@westeros:~/source/app/memorystone$ git st
    # On branch v3
    nothing to commit (working directory clean)
    jaime@westeros:~/source/app/memorystone$ vi config.yaml 
    jaime@westeros:~/source/app/memorystone$ vi index.wsgi 
    jaime@westeros:~/source/app/memorystone$ git df
    diff --git a/config.yaml b/config.yaml
    index 658ce65..c645699 100644
    --- a/config.yaml
    +++ b/config.yaml
    @@ -1,2 +1,2 @@
     name: memorystone
    -version: 2
    +version: 3
    diff --git a/index.wsgi b/index.wsgi
    index d2df150..7157797 100644
    --- a/index.wsgi
    +++ b/index.wsgi
    @@ -4,6 +4,6 @@ def app(environ, start_response):
         status = '200 OK'
         response_headers = [('Content-type', 'text/plain')]
         start_response(status, response_headers)
    -    return ['Hello, world! saecloud deploy']
    +    return ['Hello, world! -v3']
     
     application = sae.create_wsgi_app(app)
    jaime@westeros:~/source/app/memorystone$ git ci -am "Fix on v3"
    [v3 a6e6c65] Fix on v3
     2 files changed, 2 insertions(+), 2 deletions(-)
    jaime@westeros:~/source/app/memorystone$ saecloud deploy
    Deploying http://3.memorystone.sinaapp.com
    Updating cache
    Finding changes
    Pushing to server...  done


    jaime@westeros:~/source/app/memorystone$ git branch
      master
    * v3
    jaime@westeros:~/source/app/memorystone$ git co master
    Switched to branch 'master'
    jaime@westeros:~/source/app/memorystone$ vi index.wsgi 
    jaime@westeros:~/source/app/memorystone$ git df
    diff --git a/index.wsgi b/index.wsgi
    index d2df150..5704e33 100644
    --- a/index.wsgi
    +++ b/index.wsgi
    @@ -4,6 +4,6 @@ def app(environ, start_response):
         status = '200 OK'
         response_headers = [('Content-type', 'text/plain')]
         start_response(status, response_headers)
    -    return ['Hello, world! saecloud deploy']
    +    return ['Hello, world! -v2']
     
     application = sae.create_wsgi_app(app)
    jaime@westeros:~/source/app/memorystone$ git ci -am "Fix on v2"
    [master c6a90a4] Fix on v2
     1 files changed, 1 insertions(+), 1 deletions(-)
    jaime@westeros:~/source/app/memorystone$ saecloud deploy
    Deploying http://2.memorystone.sinaapp.com
    Updating cache
    Finding changes
    Pushing to server...  done
    jaime@westeros:~/source/app/memorystone$ git branch
    * master
      v3
    jaime@westeros:~/source/app/memorystone$ saecloud deploy
    Deploying http://2.memorystone.sinaapp.com
    Updating cache
    Finding changes
    No changes found
    jaime@westeros:~/source/app/memorystone$


注意:

- 如果代码量较大，则上传时间较慢，请耐心等待

- 不推荐混合使用saecloud deploy和svn
  
  虽然saecloud deploy部署之前会自动更新代码，但是如果有代码冲突则会导致本地状态不一致。

  解决办法为删除本地cache目录::
    
    rm -rf ~/.saecloud

- saecloud deploy 分离了部署和代码管理，导致用户不能像原来的svn方式那样，在不同机器之间共享代码版本历史。
  请使用你的vcs工具在不同机器之间同步代码。


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
