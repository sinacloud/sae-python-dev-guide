可用服务列表
=========================

注意：MySQL, TaskQueue, Memcache, KVDB 服务需开启才能使用，请在前端管理界面 `服务管理` 中开启并初始化。

访问互联网
-------------

直接使用urllib, urllib2或者httplib模块访问网络资源即可。

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


TaskQueue, Cron
---------------

什么是任务
~~~~~~~~~~~~~
出于安全性考虑，SAE不支持执行一段任意的代码程序。SAE的cron，和unix的cron意义不同，没有相关联的程序。

SAE的任务，实际上对应于一个URL地址。SAE worker节点每请求一次该URL，就算执行一次任务。
真正的任务处理代码，是app中处理该URL的handler。

任务执行有两种方式: Taskqueue 动态执行任务, Cron 定时执行任务

任务的执行情况可以在日志中心>TaskQueue栏中查询。

Taskqueue
~~~~~~~~~~~~~~

.. py:function:: add_task(queue_name, url, payload=None) 
   :module: sae.taskqueue

   快速添加任务    

   queue_name: 任务队列的名称

   url: 任务的url，如： /tasks/task_name

   payload: 可选，如果payload存在且不为None，则该任务为一POST任务，payload会作为请求
   的POST的数据。


.. py:class:: Task(url, payload=None, **kwargs)

   Task类
     
   url: 任务的url，如： /tasks/task_name

   payload: 可选, 如果payload存在且不为None，则该任务为一POST任务，payload会作为请求
   的POST的数据。

   delay: 可选，设置任务延迟执行的时间，单位为秒，最大可以为600秒。

   prior: 可选，如果设置为True，则任务会被添加到任务队列的头部。
 
.. py:class:: TaskQueue(name, auth_token=None)
   :module: sae.taskqueue

   TaskQueue类

   name: 任务队列的名称。

   auth_token: 可选, 一个包含两个元素的元组 (access_key, secretkey_key)。
    
   .. py:method:: add(task)

      添加一个任务
          
      task: 添加的任务，可以为单个Task任务，也可以是一个Task列表。

   .. py:method:: size()

      获取当前队列中还有多少未执行的任务。


Example:

1. 添加一个任务。   ::
    
    from sae.taskqueue import Task, TaskQueue

    queue = TaskQueue('queue_name')
    queue.add(Task("/tasks/foo"))

2. 添加一个POST任务。   ::

    queue.add(Task("/tasks/bar", "data"))

3. 批量添加任务。   ::

    tasks = [Task("/tasks/update", user) for user in users]
    queue.add(tasks)

4. 快速添加任务。   ::

    from sae.taskqueue import add_task
    add_task('queue_name', '/tasks/push', 'msg')

..  note:: 

    任务的url现在已经改为相对的url，目前兼容绝对url，但是不推荐使用。 
    任务默认使用GET方式请求，如果Task带有payload参数且不为None则使用POST方式请求。

Cron
~~~~~~~~~~~~~~~~

App的配置文件为 config.yaml. Cron的执行状态可在应用的管理界面 服务管理->
Cron中查看。

+   添加Cron:

    编辑config.yaml文件中，增加cron段，例如：   ::

        name: crontest
        version: 1
        cron:
          - description: cron_test
            url: /cron/make
            schedule: */5 * * * *

    上面的示例添加了一个cron任务，
    该任务每5分钟执行`http://crontest.sinaapp.com/cron/make`一次。

+   删除cron:

    删除config.yaml中对应的cron描述段即可就行。

+   语法字段含义

    ..  attribute:: url

        cron任务的url。例如 `/relative/url/to/cron` 。
     
    ..  attribute:: schedule

        任务描述，也就是何时执行这个cron，支持unix crontab语法。例如：  ::

               # 每天00：05分执行
               5 0 * * *
               # 每月1号的14：15分执行
               15 14 1 * *
               # 每个工作日的晚上10点执行
               0 22 * * 1-5
               # 每分钟执行一次
               */1 * * * *

        具体的语法规则可以参考man手册，`man 5 crontab`。
        
    ..  attribute:: description

        可选。任务的说明，默认为空。
     
    ..  attribute:: timezone

        可选。默认为Beijing，目前支持：Beijing, NewYork, London, Sydney, Moscow, Berlin
     
    ..  attribute:: login

        可选。http basic auth设置，格式： `用户名@密码`
     
    ..  attribute:: times

        可选。设置cron最大执行的次数，默认没有次数限制。

..  warning::

    Cron使用POST方式请求URL。

什么是POST和GET？请见 http://en.wikipedia.org/wiki/HTTP#Request_methods


登录和CRSF
~~~~~~~~~~~~~~~~~~~~

SAE任务处理节点只是简单的请求任务URL，对于除http basic auth之外的登录信息，一无所知，故务必确认你的URL
可以不用登录直接访问。

http basic auth虽然支持，但是不推荐使用。 要保护任务URL不被外界访问，请使用IP白名单。

如果你在任务URL的POST处理程序中开启了CRSF，则会导致403认证失败错误。请在任务处理程序中关闭CRSF功能，涉及框架: Django, Flask等。

什么是CRSF？ http://en.wikipedia.org/wiki/Cross-site_request_forgery


如何保护任务URL
~~~~~~~~~~~~~~~~~~
为保护cron，taskqueue对应的url，可在config.yaml配置允许访问的IP地址。

建议将所有taskqueue，cron的url都挂载到/backend/下面::

   /backend/
   /backend/taskqueue/
   /backend/cron

SAE内部节点IP范围: 10.0.0.0/8，如下配置只允许SAE内部节点访问::

    - hostaccess: if(path ~ "/backend/") allow "10.0.0.0/8"

请确保SAE内部节点在白名单内，否则将无法正常执行。


Cron 完整示例
~~~~~~~~~~~~~~~~~~~
每五分钟请求一次 /backend/cron/update URL

Flask URL 处理程序::

    import pylibmc
    import datetime

    from appstack import app

    mc = pylibmc.Client(['localhost'])

    @app.route('/backend/cron/update', methods=['GET', 'POST'])
    def update():
        update_time = mc.get('update_time')
        mc.set("update_time", str(datetime.datetime.now()))

        return update_time

config.yaml::

    name: appstack
    version: 4

    cron:
    - url: /backend/cron/update
      schedule: */5 * * * *

    handle:
    - hostaccess: if(path ~ "/backend/") allow "10.0.0.0/8"


原有的PHP文档
~~~~~~~~~~~~~~~~~
仅供参考

Taskqueue http://sae.sina.com.cn/?m=devcenter&catId=205

Cron http://sae.sina.com.cn/?m=devcenter&catId=195

AppConfig http://sae.sina.com.cn/?m=devcenter&catId=193 


Mail
-----------

..  py:class:: EmailMessage(**kwargs)
    :module: sae.mail

    EmailMessage类

    参数同下面的initialize

    ..  py:method:: initialize(\**kwargs)

        初始化邮件的内容。

        to: 收件人列表，多个收件人之间用逗号隔开。

        subject: 邮件的标题。

        body/html: 邮件正文。如果内容为纯文本，使用body，如果是html则使用html。

        smtp: smtp服务器的信息。是一个包含5个元素的tuple。
        (smtp主机，smtp端口， 用户名，密码，是否启用TLS）。

        attachments: 可选。邮件的附件，必须为一个list，list里每个元素为一个
        tuple，tuple的第一个元素为文件名，第二个元素为文件的内容。

    ..  py:method:: send

        提交邮件发送请求至后端服务器。

    ..  py:method:: __setattr__(attr, value)

        attr: 属性名。 value: 属性的值。

..  py:function:: send_mail(to, subject, body, smtp, **kwargs)
    :module: sae.mail

    快速发送邮件。

    字段的意义同EmailMessage.initialize()。
    

Examle:

1.  快速发送一份邮件 ::

        from sae.mail import send_mail

        send_mail("katherine@vampire.com", "invite", "to tonight's party"
                  ("smtp.vampire.com", 25, "damon@vampire.com", "password", False))

2.  发送一封html格式的邮件 ::

        from sae.mail import EmailMessage

        m = EmailMessage()
        m.to = 'damon@vampire.com'
        m.subject = 'Re: inivte'
        m.html = '<b>my pleause!</b>'
        m.smtp = ('smtp.vampire.com', 25, 'katherine@vampire.com', 'password', False)
        m.send()

3.  使用Gmail SMTP  ::

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

..  py:class:: Object(data, **kwargs)
    :module: sae.storage

    Object类

    data: Object的内容。

    expires: 设置Object在浏览器客户端的过期时间，格式同Apache的Expires格式：
    http://httpd.apache.org/docs/2.0/mod/mod_expires.html

    content_type: 设置Object的Conent-Type Header。

    content_encoding: 设置Object的Cotent-Encoding Header。

..  py:class:: Client(accesskey=ACCESS_KEY, secretkey=SECRET_KEY, prefix=APP_NAME)
    :module: sae.storage

    Client类

    .. py:method:: put(domain, key_name, object)

       将object存到某个domain中。返回object的public url。

    .. py:method:: get(domain, key_name)

       返回domain中名为key_name的对象。

    .. py:method:: stat(domain, key_name)

       返回domain中名为key_name的对象属性，返回值为一个dict。

    .. py:method:: delete(domain, key_name)

       删除domain中名为key_name的对象。

    .. py:method:: list(domain)

       返回domain中所有对象的列表。

    .. py:method:: list_domain():

       返回所有domain的列表。

    .. py:method::  url(domain, key_name)

       返回domain中key_name的对象的public url。

Example ::

    import sae.storage

    # 初始化一个Storage客户端。
    s = sae.storage.Client()

    # LIST所有的domain 
    s.list_domain()

    # PUT object至某个domain下面，put操作返回object的public url。
    ob = sae.storage.Object('pieces of data')
    s.put('domain-name', 'object-name', ob)

    # 设置object的属性
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


KVDB(TBD)
----------

开启和关闭
~~~~~~~~~~~~

http://sae.sina.com.cn/?m=kv

kvdb服务禁用后会清除所有数据，请谨慎操作。

sae.kvdb
~~~~~~~~~

..  py:class:: Error
    :module: sae.kvdb

    通用错误

..  py:class:: RouterError
    :module: sae.kvdb

    路由meta信息错误

..  py:class:: StatusError
    :module: sae.kvdb

    kvdb状态不为OK

..  py:class:: KVClient(**kw)
    :module: sae.kvdb

    KVDB客户端封装，基于python-memcached-1.48 memcache.Client，大多数method使用方法相同。
    如果不能成功创建KVClient，则抛出 sae.kvdb.Error 异常。

    kw: 传递给memcache.Client的keyword参数

    .. py:method:: set(key, val, time=0, min_compress_len=0)

        设置key的值为val，成功则返回True

        time 该key的超时时间，请参阅memcached协议Storage commands:
        http://code.sixapart.com/svn/memcached/trunk/server/doc/protocol.txt

        min_compress_len 启用zlib.compress压缩val的最小长度，如果val的长度大于此值
        则启用压缩，0表示不压缩。

    .. py:method:: add(key, val, time=0, min_compress_len=0)

        同set，但只在key不存在时起作用

    .. py:method:: replace(key, val, time=0, min_compress_len=0)

        同set，但只在key存在时起作用

    .. py:method:: delete(key, time=0)

        删除key，成功返回1，失败返回0。

        time 为后续多少秒内set/update操作会失败。 

    .. py:method:: get(key)

        获取key的值，失败则返回None

    .. py:method:: get_info()

        获取本应用kvdb统计数据，返回一个字典::

            {
                'outbytes': 126, 
                'total_size': 3, 
                'inbytes': 180, 
                'set_count': 60,
                'delete_count': 21, 
                'total_count': 1, 
                'get_count': 42
            }

    .. py:method:: disconnect_all()
        
        关闭kvdb连接

示例代码
~~~~~~~~~

::

    import sae.kvdb

    kv = sae.kvdb.KVClient()

    k = 'foo'
    kv.set(k, 2)
    kv.delete(k)

    kv.add(k, 3)
    kv.get(k)

    kv.replace(k, 4)
    kv.get(k)

    print kv.get_info()

参考 http://sae.sina.com.cn/?m=devcenter&catId=199

