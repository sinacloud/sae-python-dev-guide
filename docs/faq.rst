FAQ
===============

怎么寻求帮助
-------------------------

http://www.douban.com/group/topic/26638508/


什么是app版本
---------------

SAE app 代码以数字标识版本，如pythondemo应用有4个版本::

    jaime@westeros:~/source/chenfeng/pythondemo$ ls
    1  2  3  4

代码必须被放到某个版本数字目录里，默认为版本 1，可以在网页界面更改。

改变默认版本之后，请确保当前版本路径在sys.path最前面，防止误导入到旧版本的模块

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

.. note:: 在header已经发出的情况下，异常在浏览器中可能显示不出来，请查看日志。


Python新手？入门教程
--------------------------
笨办法学Python, Learn Python The Hard Way
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
作者: Zed Shaw, 译者: wangdingwei82@gmail.com

http://readthedocs.org/docs/learn-python-the-hard-way-zh_cn-translation/en/latest/index.html


Python 2.6.7 官方教程
~~~~~~~~~~~~~~~~~~~~~~~~~~
http://docs.python.org/release/2.6.7/tutorial/index.html

模块索引
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Python编程必备书签

http://docs.python.org/release/2.6.7/modindex.html


怎么使用邀请码 
------------------------------------------------------------------ 
首先，你必须有一个sae帐户，如果没有请在 http://sae.sina.com.cn 注册。 

其次，你需要正确设置你sae帐户的安全邮箱，请见 http://appstack.sinaapp.com/invite/。 

然后，打开邀请入口， http://appstack.sinaapp.com/invite/  ，输入邀请码。 
如果你收到的邀请码是链接形式，直接点击就行。 

系统完成授权需5分钟左右。之后你可直接创建python应用，并无邮件通知。 

如果按上述步骤操作仍有问题，请发帖说明。 

如果你在输入邀请码之前没有sae帐户，没有设置安全邮箱，或设置了错误的 
安全邮箱，邀请码仍是有效的。请注册帐户，修改安全邮箱，等待5分钟左右再试。 


没有邀请码？试试等待队列
------------------------------
http://appstack.sinaapp.com/queue


没有我要使用的包，怎么办？ 
------------------------------------------ 
Don't panic.

使用virtualenv管理依赖关系
http://appstack.sinaapp.com/static/doc/release/testing/runtime.html#virtualenv


关于svn的问题 
--------------------------- 

+++++++++++++++++++千万不要用svn cp，mv。You're warned.++++++++++++++ 

http://sae.sina.com.cn/?m=devcenter&catId=211 

大文件，文件数多上传 
http://www.douban.com/group/topic/23353500/ 

bug 静态目录不支持多级？ 
http://www.douban.com/group/topic/23692928/ 

建议遇到奇怪svn错误，可以： 

1. 重新在本地新建目录，检出干净的svn 

2. 或者先保存代码，然后删除该版本，重新导入 

你也许需要新建一个版本，默认版本无法删除。 


WTF！ MySQL gone away 
---------------------------------------- 
MySQL连接超时时间为30s，所以你需要在代码中检查是否超时，是否需要重连。

【bug？】我用tornado db连接 出现了mysql gone away... 
http://www.douban.com/group/topic/23673391/ 

mysql中创建表的问题 
http://www.douban.com/group/topic/23689631/ 

flask-sqlalchemy 如何在每次请求时重新连接数据库
http://www.douban.com/group/topic/24103570/


资费说明
---------------
http://sae.sina.com.cn/?m=devcenter&catId=155


如何区分本地开发环境和线上环境？
-------------------------------------

一个可靠的方法::

    if 'SERVER_SOFTWARE' in os.environ: 
        # SAE 
    else: 
        # Local 

