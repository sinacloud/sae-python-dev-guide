FAQ
===============


怎么寻求帮助
-------------------------

关于SAE Python相关服务的问题可以在以下地方提问。

* `SAE Python邮件列表`_ （推荐）

  订阅邮件列表
  发送邮件至： sae-python+subscribe@googlegroups.com
  
  退订邮件列表
  发送邮件至： sae-python+unsubscribe@googlegroups.com
  
  发表主题
  发送邮件至： sae-python@googlegroups.com
  
  订阅和退订时发送空邮件即可。如果想修改订阅方式，可以登录Google论坛后在设置中进行更改。


* `SAE Python豆瓣小组 <http://www.douban.com/group/topic/26638508/>`_

关于Python编程的其它问题，推荐到 `CPyUG邮件列表`_ 和 `Python编程豆瓣小组`_ 寻求帮助。

.. _SAE Python邮件列表: http://groups.google.com/group/sae-python
.. _CPyUG邮件列表: http://groups.google.com/group/python-cn?hl=zh-CN
.. _Python编程豆瓣小组: http://www.douban.com/group/python/

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

* 笨办法学Python, Learn Python The Hard Way

  作者: Zed Shaw, 译者: wangdingwei82@gmail.com

  http://readthedocs.org/docs/learn-python-the-hard-way-zh_cn-translation/en/latest/index.html

* Python 2.6.7 官方教程

  http://docs.python.org/release/2.6.7/tutorial/index.html

* Python模块索引

  http://docs.python.org/release/2.6.7/modindex.html

没有我要使用的包，怎么办？ 
------------------------------------------ 

Don't panic.  

对于pure python的package，See :ref:`howto-use-sae-python-with-virtualenv`

对于含有c extension的package，目前SAE还无法直接支持，如果需要这些package，可以申请预装。

`预装申请`_

.. _预装申请: https://github.com/SAEPython/saepythondevguide/issues/new

.. note::

   很多package对package里的c extension都会提供一个python的版本，这类package在sae上也可以
   直接使用，只是速度上相对于使用c extension会稍慢一点。


如何使用新浪微博API
----------------------

+   使用 `weibopy`_

    该模块已经内置，可以直接使用。 完整示例请参考： `examples/weibo`_  。

+   使用 `sinaweibopy`_ (推荐)

    新浪微博API OAuth 2 Python客户端

.. _weibopy: http://code.google.com/p/sinatpy/
.. _examples/weibo: https://github.com/SAEPython/saepythondevguide/tree/master/examples/weibo/1
.. _sinaweibopy: http://open.weibo.com/wiki/SDK#Python_SDK


如何在Cron中使用微博API
------------------------

因为现在weibo api需要提供调用者的ip（合法的公网ip），sae默认提供的是http请求的client的ip，
但是对于cron和taskqueue，由于是sae的内部请求，无法获取公网ip。所以需要用户手工设置一个。
设置方法如下： ::

    import os
    os.environ['REMOTE_ADDR'] = 调用者公网ip

请务必将这段代码放在请求处理代码执行的必经路径上。比如在Flask中：::

    @app.before_request
    def before_request():
        import os
        os.environ['REMOTE_ADDR'] = 调用者公网ip

Django框架下数据库的主从读写
-----------------------------

参见Django官方文档 `Multiple databases`_

.. _Multiple databases: https://docs.djangoproject.com/en/1.2/topics/db/multi-db/#multiple-databases

关于svn的问题 
--------------------------- 

.. warning:: 不要使用svn cp，mv，目前还不支持这两个操作。

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

