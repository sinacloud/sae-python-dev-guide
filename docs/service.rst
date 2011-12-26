可用服务列表
=========================

注意：MySQL, TaskQueue, Memcache, KVDB 服务需开启才能使用，请在前端管理界面 `服务管理` 中开启并初始化。

访问互联网
-------------
目前仅支持通过urllib2模块，urllib2.urlopen访问网络资源，其他如httplib,
urllib没有开放网络权限。故其他网络服务客户端封装，只能使用urllib2模块。


MySQL
------------

连接信息
~~~~~~~~~~

MySQL 连接超时时间为30s 。

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

不推荐直接使用这些KEY信息。

http://sae.sina.com.cn/?m=devcenter&catId=192

数据库导入
~~~~~~~~~~~~~~

创建数据表::
    
    django-admin.py sqlall all-installed-app-names > some-file
    
开发可使用本地mysql数据库，在发布时将其导入到SAE线上数据库:

#. 使用mysqldump或者phpMyAdmin等工具从本地数据库导出数据库。
#. 进入SAE后台应用管理>服务管理>MySQL页面，初始化MySQL。
#.  进入管理MySQL页面，选择导入，导入刚才导出的sql文件即可。


导入时如果出现下面的错误::

    Error 
    SQL query: 

    -- 
    -- Dumping data for table `***` 
    -- 
    LOCK TABLES `***` WRITE ; 


    MySQL said: 

    #1044 - Access denied for user '****'@'10.67.15.%' to database 'app_***'

请把要导入的sql文件中，所有LOCK, UNLOCK语句全部删除并重试。


http://pythondemo.sinaapp.com/admin/ root:root

http://pythondemo.sinaapp.com/demo/

字符集问题
~~~~~~~~~~~
在管理界面创建数据表，默认字符集为utf8，也可设为其他编码。

如果你是在本地开发环境建立的数据表，请确保使用utf8。在管理界面导入本地数据库时，
也可完成字符集的转换。


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

使用Gmail SMTP
~~~~~~~~~~~~~~~

    import sae.mail

    sae.mail.send_mail(to, subject, body,
            ('smtp.gmail.com', 587, from, passwd, True))

Memcache
-----------
请在前端管理界面启用Memcache服务。

SAE Python使用 http://sendapatch.se/projects/pylibmc/ 作为mc客户端。
不同之处在于，创建Client时不用指定servers。 

示例代码::

    import pylibmc

    mc = pylibmc.Client()
 
    mc.set("foo", "bar")
    value = mc.get("foo")
 
    if not mc.get('key'):
        mc.set("key", "1")
    mc.incr("key")

文档参考:

http://sendapatch.se/projects/pylibmc/

详细用法和 python-memcached 基本一样，可参考下面安装包中的 memcache.html 文件

http://ftp.tummy.com/pub/python-memcached/old-releases/python-memcached-1.48.tar.gz

Storage
----------

Storage是SAE为开发者提供的分布式文件存储服务，用来存放用户的持久化存储的文件。
用户需要先在在线管理平台创建Domain，每一个domain下面包含了你上传的数据。 

详细说明
http://sae.sina.com.cn/?m=devcenter&catId=204

API操作：   ::

    import sae.storage

    # 初始化一个Storage客户端。
    s = sae.storage.Client()

    # LIST所有的domain 
    s.list_domain()

    # PUT object至某个domain下面，put操作返回object的public url。
    ob = sae.storage.Object('pieces of data')
    s.put('domain-name', 'object-name', ob)

    # 设置object的属性
    # expires: 设置object的浏览器缓存超时，功能格式与Apache的Expires配置相同
    # content_type: 设置object header中的Content-Type字段。（注：此处的type和storage
    #   后台面板类型一栏的值没有任何关系）。
    # content_encoding: 设置object header中的Content-Encoding字段。
    ob = sae.storage.Object('pieces of data',   \
      expires='A3600', content_type='text/html', content_encoding='gzip')
    s.put('domain-name', 'object-name', ob)

    # GET某个domain下的object
    ob = s.get('domain-name', 'object-name')
    data = ob.data

    # 获取object的属性信息
    ob = s.stat('domain-name', 'object-name')

    # 获取object的public url 
    url = s.url('domain-name', 'object-name')

    # DELETE一个object
    s.delete('domain-name', 'object-name')

    # LIST一个domain下所有的object 
    s.list('domain-name')

Cron
-----------
请参阅标准SAE文档 http://sae.sina.com.cn/?m=devcenter&catId=195

