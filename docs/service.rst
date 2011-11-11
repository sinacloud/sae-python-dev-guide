可用服务列表
=========================

访问互联网
-------------
目前仅支持通过urllib2模块，urllib2.urlopen访问网络资源，其他如httplib,
urllib没有开放网络权限。故其他网络服务客户端封装，只能使用urllib2模块。


MySQL
------------

连接信息
~~~~~~~~~~

有两种方式获取mysql的连接信息，推荐使用sae.const中定义的常量::

    import sae.const

    sae.const.MYSQL_DB
    sae.const.MYSQL_USER
    sae.const.MYSQL_PASS
    sae.const.MYSQL_HOST
    sae.const.MYSQL_PORT   #请根据框架要求自行转换为int
    sae.const.MYSQL_HOST_S #salve mysql server

下面的方式已不推荐使用::

        
        import sae.core
        app = sae.core.Application()

        DATABASES = {
            'default': {
                'ENGINE': 'mysql',
                'NAME': app.mysql_db,
                'USER': app.mysql_user,
                'PASSWORD': app.mysql_pass,
                'HOST': app.mysql_host,
                'PORT': app.mysql_port,
            }
        }

MySQL数据库静态信息 ::

    SAE_MYSQL_HOST_M = 'w.rdc.sae.sina.com.cn'
    SAE_MYSQL_HOST_S = 'r.rdc.sae.sina.com.cn'
    SAE_MYSQL_PORT = '3307' 
    
    mysql_db = 'app_%s' % app_name
    mysql_user = access_key
    mysql_pass = secret_key

应用的access_key, secret_key，可在应用管理界面的汇总信息中看到。

http://sae.sina.com.cn/?m=devcenter&catId=192

数据库导入
~~~~~~~~~~~~~~

创建数据表::
    
    django-admin.py sqlall all-installed-app-names > some-file
    
开发可使用本地mysql数据库，在发布时将其导入到SAE线上数据库:

#. 使用mysqldump或者phpMyAdmin等工具从本地数据库导出数据库。
#. 进入SAE后台应用管理>服务管理>MySQL页面，初始化MySQL。
#.  进入管理MySQL页面，选择导入，导入刚才导出的sql文件即可。

http://pythondemo.sinaapp.com/admin/ root:root

http://pythondemo.sinaapp.com/demo/


TaskQueue
---------------
TaskQueue is a distributed task queue service provided by SAE for developers as
a simple way to execute asynchronous user tasks.

http://sae.sina.com.cn/?m=devcenter&catId=205

Example:

1. Add a GET task::
    
    from sae.taskqueue import Task, TaskQueue

    queue = TaskQueue('queue_name')
    queue.add(Task("http://blahblah/blah"))

2. Add a POST task::

    queue.add(Task("http://blahblah/blah", "postdata"))

3. Add a bundle of tasks::

    tasks = [Task("http://blahblah/blah", d) for d in datas]
    queue.add(tasks)

4. A simple way to add task::

    from sae.taskqueue import add_task
    add_task('queue_name', 'http://blahblah/blah', 'postdata')

Mail
-----------

Provides functions for application developers to deliver mail messages 
for their applications. Currently we only support send mail through SMTP 
asynchronously.

Examle:

1. Send a simple plain-text message::

    from sae.mail import send_mail

    send_mail('recipient@sina.com', 'subject', 'plain text',
              ('smtp.sina.com', 25, 'me@sina.com', 'password', False))

2. Send a HTML-format message::

    from sae.mail import EmailMessage

    m = EmailMessage()
    m.to = 'recipient@sina.com'
    m.subject = 'unforgivable sinner'
    m.html = '<b>darling, please, please forgive me...</b>'
    m.smtp = ('smtp.sina.com', 25, 'me@sina.com', 'password', False)
    m.send()
