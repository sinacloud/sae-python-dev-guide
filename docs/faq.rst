FAQ
===============

BUG反馈以及问题求助
-------------------------

关于SAE Python相关服务的问题可以在以下地方反馈和提问。

* `SAE Python邮件列表`_ （推荐）

  订阅邮件列表
  发送邮件至： sae-python+subscribe@googlegroups.com
  
  退订邮件列表
  发送邮件至： sae-python+unsubscribe@googlegroups.com
  
  发表主题
  发送邮件至： sae-python@googlegroups.com
  
  订阅和退订时发送空邮件即可。如果想修改订阅方式，可以登录Google论坛后在设置中进行更改。


* `SAE Python豆瓣小组（一些旧帖子的存档） <http://www.douban.com/group/pythoncitadel/>`_

关于Python编程的其它问题，推荐到 `CPyUG邮件列表`_ 寻求帮助。

.. _SAE Python邮件列表: http://groups.google.com/group/sae-python
.. _CPyUG邮件列表: http://groups.google.com/group/python-cn?hl=zh-CN

如何调试
------------

复杂程序建议您本地调试成功后，再上传运行。

SAE Python 版本为 2.7.3，本地调试时注意不要使用高于此版本的python。

如果你使用内置的第三方库，本地调试时最好使用同样的版本。

对于50x页面，如果异常被web框架捕获，则需要打开web框架的调试开关，查看详细的异常信息。如果异常被python server捕获，
python server会直接在浏览器中打印出异常。

.. note:: 在header已经发出的情况下，异常在浏览器中可能显示不出来，请查看日志。


没有我要使用的包怎么办
------------------------

对于纯python的package，See :ref:`howto-use-sae-python-with-virtualenv`

对于含有c extension的package，目前SAE还无法直接支持，如果需要这些package，可以申请预装。

`预装申请`_

.. _预装申请: https://github.com/SAEPython/saepythondevguide/issues/new

.. note::

   很多package对package里的c extension都会提供一个python的fallback版本，这类package在sae上也可以
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

遇到奇怪的SVN错误，可以： 

+ 重新在本地新建目录，检出干净的svn 
+ 或者先保存代码，然后删除该版本，重新导入 

你也许需要新建一个版本，默认版本无法删除。 


MySQL gone away问题
----------------------

MySQL连接超时时间为30s，不是mysql默认的8小时，所以你需要在代码中检查是否超时，是否需要重连。

如何区分本地开发环境和线上环境
-------------------------------------
::

    if 'SERVER_SOFTWARE' in os.environ: 
        # SAE 
    else: 
        # Local 

