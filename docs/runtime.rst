SAE Python环境
=======================

环境信息
----------

* 当前目录
  
    该版本app代码所在目录，即index.wsgi 所在目录， 如 /data1/www/htdocs/115/longtalk/1。

    该目录已经在 sys.path 中。

    推荐使用__file__属性，不要依靠os.getcwd()的值

* 应用版本

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
* 除临时文件，应用自身所在目录外，不可访问本地文件系统。本地文件系统不可写入。
* 不能动态加载C扩展，即.so，.dll等格式的模块不能使用
* urllib不能访问外网，请使用urllib2

文件系统
--------------
可读: 本app根目录，可以读取本app其他版本的目录

可写目录: sae.core.get_tmp_dir(), 暂不可用


代码加载机制
--------------
svn commit 会自动触发代码重新加载，不需再手动修改index.wsgi。


错误输出
---------
打印到stderr的信息，会被自动记录到日志中，可在管理界面 应用调优->日志中心->HTTP
中查看，类别为debug。

此功能可配合 logging 模块使用，方便的打印日志。请参阅:
http://docs.python.org/library/logging.handlers.html#streamhandler
 

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

如果有404错误，试试访问  http://$appname.sinaapp.com/debug 

未捕获的WSGI异常，将会被打印到浏览器上。
注意：在header已经发出的情况下，异常处理可能不会工作。

如何寻求帮助？
http://www.douban.com/group/topic/26638508/


使用dev_server进行调试
-------------------------

注意：本工具仅为应用开发便利之用，与真实的sae环境相差较大。

dev_server地址  https://github.com/SAEPython/saepythondevguide

下载
~~~~~~~
使用git clone ::

    git clone http://github.com/SAEPython/saepythondevguide.git

或打包下载: https://github.com/SAEPython/saepythondevguide/zipball/master


Install
~~~~~~~~~~~~
::

    cd dev_server
    sudo python setup.py install

由于预装模块太多，全部安装太过耗时，故所有依赖关系已在 setup.py 中注掉，
请自行使用pip安装你要使用的框架，注意版本号应于SAE内置的相同。


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


使用virtualenv管理依赖关系
-------------------------------------------

virtualenv 可以有效解决在同一个python版本下面运行多个第三方包版本冲突的问题，
官方文档:

http://pypi.python.org/pypi/virtualenv

当你的应用依赖多个第三方包时，可参考下面的流程。

安装virtualenv
~~~~~~~~~~~~~~~~~

::
    
    pip install virtualenv


创建目录
~~~~~~~~~~~~~~~

创建应用根目录::

    jaime@westeros:~/source/app$ mkdir memorystone
    jaime@westeros:~/source/app$ cd memorystone/
    jaime@westeros:~/source/app/memorystone$ ls

创建虚拟环境目录::

    jaime@westeros:~/source/app/memorystone$ virtualenv memorystone
    New python executable in memorystone/bin/python
    Installing setuptools............done.
    Installing pip...............done.
    jaime@westeros:~/source/app/memorystone$ ls
    memorystone
    jaime@westeros:~/source/app/memorystone$ ls memorystone/
    bin  include  lib  local

启动虚拟环境::


    jaime@westeros:~/source/app/memorystone$ source memorystone/bin/activate
    (memorystone)jaime@westeros:~/source/app/memorystone$ ls
    memorystone

在提示符里可看到虚拟环境的名字, 实际上是bin/activate上层目录的名字。


建立应用版本目录和index.wsgi::

    (memorystone)jaime@westeros:~/source/app/memorystone$ mkdir 1
    (memorystone)jaime@westeros:~/source/app/memorystone$ cd 1
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ ls
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ touch index.wsgi
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ ls
    index.wsgi
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ 

OK, 编码开始。

安装依赖关系
~~~~~~~~~~~~~~~~~~~

在虚拟环境中，可以像往常一样使用pip。

安装Flask，SAE环境Flask版本为0.7.2，为保持一致，可使用::

    (memorystone)jaime@westeros:~/source/app/memorystone/1$ pip install flask==0.7.2
    Downloading/unpacking flask==0.7.2
      Downloading Flask-0.7.2.tar.gz (469Kb): 469Kb downloaded
      Running setup.py egg_info for package flask
    ....

实际安装位置在::

    (memorystone)jaime@westeros:~/source/app/memorystone$ ls memorystone/lib/python2.7/site-packages/
    easy-install.pth            jinja2                     setuptools-0.6c11-py2.7.egg  Werkzeug-0.8.2-py2.7.egg-info
    flask                       Jinja2-2.6-py2.7.egg-info  setuptools.pth
    Flask-0.7.2-py2.7.egg-info  pip-1.0.2-py2.7.egg        werkzeug

    
安装其他packages::

    (memorystone)jaime@westeros:~/source/app/memorystone/1$ pip install Flask Flask-Cache Flask-SQLAlchemy Flask-Principal Flask-WTF Flask-Mail Flask-Script Flask-Babel Flask-Themes markdown blinker
    Requirement already satisfied (use --upgrade to upgrade): Flask in /home/chenz/source/app/memorystone/memorystone/lib/python2.7/site-packages
    Downloading/unpacking Flask-Cache
   ...


看看装了些什么::

    (memorystone)jaime@westeros:~/source/app/memorystone/1$ pip freeze
    Babel==0.9.6
    Flask==0.7.2
    Flask-Babel==0.8
    Flask-Cache==0.4.0
    Flask-Mail==0.6.1
    Flask-Principal==0.2
    Flask-SQLAlchemy==0.15
    Flask-Script==0.3.1
    Flask-Themes==0.1.3
    Flask-WTF==0.5.2
    Jinja2==2.6
    Markdown==2.1.0
    SQLAlchemy==0.7.4
    WTForms==0.6.3
    Werkzeug==0.8.2
    argparse==1.2.1
    blinker==1.2
    chardet==1.0.1
    lamson==1.1
    lockfile==0.9.1
    mock==0.7.2
    nose==1.1.2
    python-daemon==1.6
    pytz==2011n
    speaklater==1.2
    wsgiref==0.1.2

    (memorystone)jaime@westeros:~/source/app/memorystone/1$ ls ../memorystone/lib/python2.7/site-packages/
    argparse-1.2.1-py2.7.egg-info      Flask_Principal-0.2-py2.7.egg-info     mock.pyc
    argparse.py                        Flask_Principal-0.2-py2.7-nspkg.pth    nose
    argparse.pyc                       Flask_Script-0.3.1-py2.7.egg-info      nose-1.1.2-py2.7.egg-info
    babel                              Flask_Script-0.3.1-py2.7-nspkg.pth     pip-1.0.2-py2.7.egg
    Babel-0.9.6-py2.7.egg-info         Flask_SQLAlchemy-0.15-py2.7.egg-info   python_daemon-1.6-py2.7.egg-info
    blinker                            Flask_SQLAlchemy-0.15-py2.7-nspkg.pth  pytz
    blinker-1.2-py2.7.egg-info         Flask_Themes-0.1.3-py2.7.egg-info      pytz-2011n-py2.7.egg-info
    ....

导出依赖关系到代码目录
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

写完代码后，可使用dev_server进行调试。如何使用dev_server，请参阅上节。

如果没什么问题，可使用pip导出依赖关系::

    (memorystone)jaime@westeros:~/source/app/memorystone/1$ pip freeze > requirements.txt
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ pip freeze > requirements.sae.txt
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ vi requirements.sae.txt 
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ diff requirements.txt requirements.sae.txt 
    2d1
    < Flask==0.7.2
    11d9
    < Jinja2==2.6
    13,15d10
    < SQLAlchemy==0.7.4
    < WTForms==0.6.3
    < Werkzeug==0.8.2
    26d20
    < wsgiref==0.1.2

flask, jinja2, wtforms等SAE已内置，所以不需要再上传，故从requirements.sae.txt中去除。

使用dev_server/bundle_local.py工具，将所有requirements.sae.txt中列出的包，根据其top_levels.txt信息，导出到本地目录::

    (memorystone)jaime@westeros:~/source/app/memorystone/1$ ls
    index.wsgi  requirements.local.txt  requirements.sae.txt  requirements.txt
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ ~/source/saepythondevguide/dev_server/bundle_local.py -r requirements.sae.txt 
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ ls 
    index.wsgi  requirements.local.txt  requirements.sae.txt  requirements.txt  virtualenv.bundle

多出了一个 virtualenv.bundle 目录，所有的包都在这里了::

    (memorystone)jaime@westeros:~/source/app/memorystone/1$ ls virtualenv.bundle/
    argparse.py  blinker  daemon    lamson    markdown  nose  requirements.txt
    babel        chardet  flaskext  lockfile  mock.py   pytz  speaklater.py
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ cat requirements.sae.txt 
    Babel==0.9.6
    Flask-Babel==0.8
    Flask-Cache==0.4.0
    Flask-Mail==0.6.1
    Flask-Principal==0.2
    Flask-SQLAlchemy==0.15
    Flask-Script==0.3.1
    Flask-Themes==0.1.3
    Flask-WTF==0.5.2
    Markdown==2.1.0
    argparse==1.2.1
    blinker==1.2
    chardet==1.0.1
    lamson==1.1
    lockfile==0.9.1
    mock==0.7.2
    nose==1.1.2
    python-daemon==1.6
    pytz==2011n
    speaklater==1.2

上传到SAE
~~~~~~~~~~~~~~~

你可以把virtualenv.bundle目录直接添加到svn。

如果文件太多，推荐压缩后再添加上传::

    (memorystone)jaime@westeros:~/source/app/memorystone/1$ cd virtualenv.bundle/
    (memorystone)jaime@westeros:~/source/app/memorystone/1/virtualenv.bundle$ zip -r ../virtualenv.bundle.zip .
      adding: lamson/ (stored 0%)
      adding: lamson/queue.py (deflated 64%)
      adding: lamson/utils.py (deflated 61%)
      adding: lamson/server.py (deflated 66%)
      ....  

    (memorystone)jaime@westeros:~/source/app/memorystone/1/virtualenv.bundle$ cd ../
    (memorystone)jaime@westeros:~/source/app/memorystone/1$ ls
    index.wsgi              requirements.sae.txt  virtualenv.bundle
    requirements.local.txt  requirements.txt      virtualenv.bundle.zip
    (memorystone)jaime@westeros:~/source/app/memorystone/1$

注意: 

- 有些包是not-zip-safe的，可能不工作，有待验证。

- 含有c扩展的package不能工作


不管是目录，还是zip，都需要在index.wsgi的最前面，导入任何模块之前，添加到sys.path中才起作用::

    import os
    import sys

    app_root = os.path.dirname(__file__)

    # 两者取其一
    sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle'))
    sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))


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
