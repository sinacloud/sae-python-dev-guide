FAQ
===============

什么是app版本
---------------

SAE app 代码以数字标识版本，如pythondemo应用有4个版本::

    jaime@westeros:~/source/chenfeng/pythondemo$ ls
    1  2  3  4

代码必须被放到某个版本数字目录里，默认为版本 1，可以在网页界面更改。

改变默认版本之后，请确保当前版本路径在sys.path最前面，防止误导入到旧版本的模块


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


怎么寻求帮助
-------------------------

http://www.douban.com/group/topic/26638508/


资费说明
---------------
http://sae.sina.com.cn/?m=devcenter&catId=155
