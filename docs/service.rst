可用服务列表
=========================

注意：MySQL, TaskQueue, Memcache, KVDB 服务需开启才能使用，请在前端管理界面 `服务管理` 中开启并初始化。

访问互联网
-------------

直接使用urllib, urllib2或者httplib模块访问网络资源即可。

默认使用sae提供的fetchurl服务来抓取网页，对于fetchurl不支持的功能（HTTP代理等），可以禁用掉fetchurl服务，
使用socket服务来处理请求。 ::

    import os
    os.environ['disable_fetchurl'] = True

MySQL
------------

连接信息
~~~~~~~~~~~

获取mysql的连接信息。

.. module:: sae.const
   :synopsis: MYSQL连接信息

::

    import sae.const

    sae.const.MYSQL_DB      # 数据库名
    sae.const.MYSQL_USER    # 用户名
    sae.const.MYSQL_PASS    # 密码
    sae.const.MYSQL_HOST    # 主库域名（可读写）
    sae.const.MYSQL_PORT    # 端口，类型为<type 'str'>，请根据框架要求自行转换为int
    sae.const.MYSQL_HOST_S  # 从库域名（只读）

下面就可以跟平常一样使用MySQL服务了，SAE Python内置了MySQLdb模块，对于MySQLdb的使用，可以参考其 `官方文档`_ 。

.. _官方文档: http://mysql-python.sourceforge.net/MySQLdb.html

注意： MySQL 连接超时时间为30s 。

数据库管理
~~~~~~~~~~~~~~

SAE支持使用PHPMyAdmin来管理Mysql，点击管理面板 `服务管理 > MySQL > 管理MySQL` 即可进入。

开发时可使用本地mysql数据库，在发布时再将其导入到SAE线上数据库中。

.. note::

   导入sql文件时，请先删除所有的LOCK, UNLOCK语句。

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

.. module:: sae.taskqueue

.. py:function:: add_task(queue_name, url, payload=None, **kws)

   快速添加任务    

   queue_name: 任务队列的名称

   url: 任务的url，如： /tasks/task_name

   payload: 可选，如果payload存在且不为None，则该任务为一POST任务，payload会作为请求
   的POST的数据。

   delay/prior: 可选，使用方法参见Task。


.. py:class:: Task(url, payload=None, **kwargs)

   Task类
     
   url: 任务的url，如： /tasks/task_name

   payload: 可选, 如果payload存在且不为None，则该任务为一POST任务，payload会作为请求
   的POST的数据。

   delay: 可选，设置任务延迟执行的时间，单位为秒，最大可以为600秒。

   prior: 可选，如果设置为True，则任务会被添加到任务队列的头部。
 
.. py:class:: TaskQueue(name, auth_token=None)

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

Cron的配置文件为 `config.yaml` ，Cron的执行状态可在应用的管理界面 `服务管理>Cron` 中查看。

+   添加Cron:

    编辑config.yaml文件中，增加cron段，例如：   ::

        name: crontest
        version: 1
        cron:
        - description: cron_test
          url: /cron/make
          schedule: "*/5 * * * *"

    上面的示例添加了一个cron任务，
    该任务每5分钟执行 `http://crontest.sinaapp.com/cron/make` 一次。

+   删除cron:

    删除config.yaml中对应的cron描述段即可就行。

+   语法字段含义

    - url

      cron任务的url。例如 `/relative/url/to/cron` 。
     
    - schedule

      任务描述，也就是何时执行这个cron，支持unix crontab语法。例如：  ::

               # 每天00：05分执行
               "5 0 * * *"
               # 每月1号的14：15分执行
               "15 14 1 * *"
               # 每个工作日的晚上10点执行
               "0 22 * * 1-5"
               # 每分钟执行一次
               "*/1 * * * *"

      具体的语法规则可以参考man手册， `man 5 crontab`_ 。
        
    - description

      可选。任务的说明，默认为空。
     
    - timezone

      可选。默认为Beijing，目前支持：Beijing, NewYork, London, Sydney, Moscow, Berlin
     
    - login

      可选。http basic auth设置，格式： `用户名@密码`
     
    - times

      可选。设置cron最大执行的次数，默认没有次数限制。

.. _man 5 crontab: http://man.he.net/man5/crontab

..  note::

    Cron使用GET方式请求URL。

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
      schedule: "*/5 * * * *"

Mail
-----------

Mail是SAE为开发者提供的邮件发送服务，用来异步发送标准SMTP邮件。Mail的日志可以在 `日志中心» Mail` 中查看。

..  module:: sae.mail

..  py:class:: EmailMessage(**kwargs)
    :module: sae.mail

    EmailMessage类

    参数同下面的initialize

    ..  py:method:: initialize(\**kwargs)

        初始化邮件的内容。

        to: 收件人，收件人邮件地址或者收件人邮件地址的列表。

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

        send_mail("katherine@vampire.com", "invite", "to tonight's party",
                  ("smtp.vampire.com", 25, "damon@vampire.com", "password", False))

2.  发送邮件给多个收件人 ::

        to = ["katherine@vampire.com", 'rebecca@vampire.com', 'elena@vampire.com']
        send_mail(to, "invite", "to tonight's party",
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

..  module:: pylibmc
    :synopsis: memcache模块

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

pylibmc接口和 `python-memcached`_ 基本兼容，可以直接替换使用。 `python-memcache文档 <_static/memcache.html>`_ 。

.. _python-memcached: http://www.tummy.com/Community/software/python-memcached/

Storage
----------

Storage是SAE为开发者提供的分布式文件存储服务，用来存放用户的持久化存储的文件。

用户需要先在在线管理平台创建Domain，每一个domain下面包含了你上传的数据。 

..  module:: sae.storage

..  py:class:: Object(data, **kwargs)

    Object类

    data: Object的内容。

    expires: 设置Object在浏览器客户端的过期时间，格式同Apache的Expires格式：
    http://httpd.apache.org/docs/2.0/mod/mod_expires.html

    content_type: 设置Object的Conent-Type Header。

    content_encoding: 设置Object的Cotent-Encoding Header。

..  py:class:: Client(accesskey=ACCESS_KEY, secretkey=SECRET_KEY, prefix=APP_NAME)

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


KVDB
----------

kvdb服务使用前需要在 `管理面板`_ 中启用，不再使用时可以在面板中禁用，禁用会删除所有数据。

.. _管理面板: http://sae.sina.com.cn/?m=kv

..  module:: sae.kvdb

..  py:class:: Error
    :module: sae.kvdb

    通用错误

..  py:class:: RouterError
    :module: sae.kvdb

    路由meta信息错误

..  py:class:: StatusError
    :module: sae.kvdb

    kvdb状态不为OK

..  py:class:: KVClient(debug=0)
    :module: sae.kvdb

    KVDB客户端基于python-memcached，大多数method使用方法相同。
    如果不能成功创建KVClient，则抛出 sae.kvdb.Error 异常。

    debug 是否输出详细调试、错误信息到日志，默认关闭

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

       从kvdb中获取一个key的值。成功返回key的值，失败则返回None

    .. py:method:: get_multi(keys, key_prefix='')

       从kvdb中一次获取多个key的值。返回一个key/value的dict。

       keys: key的列表，类型必须为list。

       key_prefix: 所有key的前缀。请求时会在所有的key前面加上该前缀，返回值里所有的key都会去掉该前缀。

    .. py:method:: get_by_prefix(prefix, max_count=100, start_key=None)

       从kvdb中查找指定前缀的 key/value pair。返回一个list，该list中每个item为一个(key, value)的tuple。

       prefix: 需要查找的key的前缀。

       max_count: 最多返回的item个数，默认为100。

       start_key: 指定返回的第一个item的key，该key不包含在返回中。

    .. py:method:: getkeys_by_prefix(prefix, max_count=100, start_key=None)

       从kvdb中查找指定前缀的key。返回符合条件的key的list。

       prefix: 需要查找的key的前缀。

       max_count: 最多返回的key的个数，默认为100。

       start_key: 指定返回的第一个key，该key不包含在返回中。

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

示例代码: ::

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

服务限制:

+ 存储空间：100G
+ 最大记录条数：1,000,000,000
+ key的最大长度：200 Bytes
+ value的最大长度：4M
+ get_multi获取的最大KEY个数：32

SOCKET
-----------------

直接使用socket模块即可。目前仅支持AF_INET, SOCK_STREAM连接，暂时不支持异步socket。bind/listen方法无法使用。

中文分词
-------------------

**分词服务请求**

SAE分词服务请求采用以下形式的HTTP网址： ::

    http://segment.sae.sina.com.cn/urlclient.php?parameters

parameters为请求参数，多个参数之间使用&分割，以下列出了这些参数和其可能的值。

* word_tag: 是否返回词性数据。0表示不返回，1表示返回，默认为0不返回。
* encoding: 请求分词的文本的编码，可以为: GB18030、UTF-8、UCS-2，默认为UTF-8。

请求分词的文本以post的形式提交。

* context: 请求分词的文本。目前限制文本大小最大为10KB。

**分词服务响应**

分词服务的响应数据为json格式，格式如下： ::

    [
        {"word":"采莲","word_tag":"171","index":"1"},
        {"word":"赋","word_tag":"170","index":"2"}
    ]

响应数据为一个list，list中每个元素为一个dict，每个dict中包含以下数据：

* index: 序列号，按在请求文本中的位置依次递增。
* word: 单词
* word_tag: 单词的词性，仅当输入parameters里word_tag为1时包含该项。

词性代码： ::

    0   POSTAG_ID_UNKNOW 未知
    10  POSTAG_ID_A      形容词
    20  POSTAG_ID_B      区别词
    30  POSTAG_ID_C      连词
    31  POSTAG_ID_C_N    体词连接
    32  POSTAG_ID_C_Z    分句连接
    40  POSTAG_ID_D      副词
    41  POSTAG_ID_D_B    副词("不")
    42  POSTAG_ID_D_M    副词("没")
    50  POSTAG_ID_E      叹词
    60  POSTAG_ID_F      方位词
    61  POSTAG_ID_F_S    方位短语(处所词+方位词)
    62  POSTAG_ID_F_N    方位短语(名词+方位词“地上”)
    63  POSTAG_ID_F_V    方位短语(动词+方位词“取前”)
    64  POSTAG_ID_F_Z    方位短语(动词+方位词“取前”)
    70  POSTAG_ID_H      前接成分
    71  POSTAG_ID_H_M    数词前缀(“数”---数十)
    72  POSTAG_ID_H_T    时间词前缀(“公元”“明永乐”)
    73  POSTAG_ID_H_NR   姓氏
    74  POSTAG_ID_H_N    姓氏
    80  POSTAG_ID_K      后接成分
    81  POSTAG_ID_K_M    数词后缀(“来”--,十来个)
    82  POSTAG_ID_K_T    时间词后缀(“初”“末”“时”)
    83  POSTAG_ID_K_N    名词后缀(“们”)
    84  POSTAG_ID_K_S    处所词后缀(“苑”“里”)
    85  POSTAG_ID_K_Z    状态词后缀(“然”)
    86  POSTAG_ID_K_NT   状态词后缀(“然”)
    87  POSTAG_ID_K_NS   状态词后缀(“然”)
    90  POSTAG_ID_M      数词
    95  POSTAG_ID_N      名词
    96  POSTAG_ID_N_RZ   人名(“毛泽东”)
    97  POSTAG_ID_N_T    机构团体(“团”的声母为t，名词代码n和t并在一起。“公司”)
    98  POSTAG_ID_N_TA   ....
    99  POSTAG_ID_N_TZ   机构团体名("北大")
    100 POSTAG_ID_N_Z    其他专名(“专”的声母的第1个字母为z，名词代码n和z并在一起。)
    101 POSTAG_ID_NS     名处词
    102 POSTAG_ID_NS_Z   地名(名处词专指：“中国”)
    103 POSTAG_ID_N_M    n-m,数词开头的名词(三个学生)
    104 POSTAG_ID_N_RB   n-rb,以区别词/代词开头的名词(该学校，该生)
    107 POSTAG_ID_O      拟声词
    108 POSTAG_ID_P      介词
    110 POSTAG_ID_Q      量词
    111 POSTAG_ID_Q_V    动量词(“趟”“遍”)
    112 POSTAG_ID_Q_T    时间量词(“年”“月”“期”)
    113 POSTAG_ID_Q_H    货币量词(“元”“美元”“英镑”)
    120 POSTAG_ID_R      代词
    121 POSTAG_ID_R_D    副词性代词(“怎么”)
    122 POSTAG_ID_R_M    数词性代词(“多少”)
    123 POSTAG_ID_R_N    名词性代词(“什么”“谁”)
    124 POSTAG_ID_R_S    处所词性代词(“哪儿”)
    125 POSTAG_ID_R_T    时间词性代词(“何时”)
    126 POSTAG_ID_R_Z    谓词性代词(“怎么样”)
    127 POSTAG_ID_R_B    区别词性代词(“某”“每”)
    130 POSTAG_ID_S      处所词(取英语space的第1个字母。“东部”)
    131 POSTAG_ID_S_Z    处所词(取英语space的第1个字母。“东部”)
    132 POSTAG_ID_T      时间词(取英语time的第1个字母)
    133 POSTAG_ID_T_Z    时间专指(“唐代”“西周”)
    140 POSTAG_ID_U      助词
    141 POSTAG_ID_U_N    定语助词(“的”)
    142 POSTAG_ID_U_D    状语助词(“地”)
    143 POSTAG_ID_U_C    补语助词(“得”)
    144 POSTAG_ID_U_Z    谓词后助词(“了、着、过”)
    145 POSTAG_ID_U_S    体词后助词(“等、等等”)
    146 POSTAG_ID_U_SO   助词(“所”)
    150 POSTAG_ID_W      标点符号
    151 POSTAG_ID_W_D    顿号(“、”)
    152 POSTAG_ID_W_SP   句号(“。”)
    153 POSTAG_ID_W_S    分句尾标点(“，”“；”)
    154 POSTAG_ID_W_L    搭配型标点左部
    155 POSTAG_ID_W_R    搭配型标点右部(“》”“]”“）”)
    156 POSTAG_ID_W_H    中缀型符号
    160 POSTAG_ID_Y      语气词(取汉字“语”的声母。“吗”“吧”“啦”)
    170 POSTAG_ID_V      及物动词(取英语动词verb的第一个字母。)
    171 POSTAG_ID_V_O    不及物谓词(谓宾结构“剃头”)
    172 POSTAG_ID_V_E    动补结构动词(“取出”“放到”)
    173 POSTAG_ID_V_SH   动词“是”
    174 POSTAG_ID_V_YO   动词“有”
    175 POSTAG_ID_V_Q    趋向动词(“来”“去”“进来”)
    176 POSTAG_ID_V_A    助动词(“应该”“能够”)
    180 POSTAG_ID_Z      状态词(不及物动词,v-o、sp之外的不及物动词)
    190 POSTAG_ID_X      语素字
    191 POSTAG_ID_X_N    名词语素(“琥”)
    192 POSTAG_ID_X_V    动词语素(“酹”)
    193 POSTAG_ID_X_S    处所词语素(“中”“日”“美”)
    194 POSTAG_ID_X_T    时间词语素(“唐”“宋”“元”)
    195 POSTAG_ID_X_Z    状态词语素(“伟”“芳”)
    196 POSTAG_ID_X_B    状态词语素(“伟”“芳”)
    200 POSTAG_ID_SP     不及物谓词(主谓结构“腰酸”“头疼”)
    201 POSTAG_ID_MQ     数量短语(“叁个”)
    202 POSTAG_ID_RQ     代量短语(“这个”)
    210 POSTAG_ID_AD     副形词(直接作状语的形容词)
    211 POSTAG_ID_AN     名形词(具有名词功能的形容词)
    212 POSTAG_ID_VD     副动词(直接作状语的动词)
    213 POSTAG_ID_VN     名动词(指具有名词功能的动词)
    230 POSTAG_ID_SPACE  空格

例： ::

    chinese_text = """
    这里填上需要分词的文本
    """

    _SEGMENT_BASE_URL = 'http://segment.sae.sina.com.cn/urlclient.php'

    payload = urllib.urlencode([('context', chinese_text),])
    args = urllib.urlencode([('word_tag', 1), ('encoding', 'UTF-8'),])
    url = _SEGMENT_BASE_URL + '?' + args
    result = urllib2.urlopen(url, payload).read()

短信
------------------

**短信服务请求**

SAE短信服务请求采用以下形式的HTTP网址： ::

    http://inno.smsinter.sina.com.cn/sae_sms_service/sendsms.php

参数采用POST的方法提交，以下列出了这些参数和其可能的值。

* mobile: 对方的手机号码。
* msg: 短信发送的内容。
* encoding: 可选。短信内容的编码格式，可以为：GB2312、UTF-8，默认为UTF-8。

**短信服务响应**

短信服务的响应为json格式，格式如下： ::

    {
        "sms": {
            "encoding": "GB2312", 
            "mobile": "18911978203", 
            "msg": "hello....."
        }, 
        "status": "\\u77ed\\u4fe1\\u63d0\\u4ea4\\u6210\\u529f"
    }

响应数据为一个dict，dict中包含以下数据:

* sms: 短信服务请求的参数。
* status：短信发送的状态。 

