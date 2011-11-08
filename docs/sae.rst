:mod:`sae` --- SAE Python扩展包
==============================================================

.. module:: sae
   :synopsis: SAE Python扩展包
.. moduleauthor:: 
.. sectionauthor:: 


本模块为在SAE上开发Python应用提供便利。

.. function:: create_wsgi_app(app)

   将标准wsgi应用封装为适宜在SAE上运行的应用


:mod:`sae.core` -- SAE核心功能模块
-------------------------------------------------

.. module:: sae.core
   :synopsis: SAE核心功能模块

.. class:: Application()

   sae app示例，可以获取诸如应用name, version, access_key, secret_key, mysql_user等信息


.. function:: get_access_key()

   获取应用access_key的另一种方法

.. function:: get_secret_key()

.. function:: get_trusted_hosts()
   
   获取可信主机列表，在此列表中的可直接访问，否则通过fetchurl服务转发

.. attribute:: environ

   wsgi应用的environ环境变量副本，只读，由sae.create_wsgi_app设置。


:mod:`sae.conf` -- SAE服务参数配置
-------------------------------------------------

.. module:: sae.conf
   :synopsis: SAE服务参数配置

.. attribute:: SAE_MYSQL_HOST_M

.. attribute:: SAE_MYSQL_HOST_S

.. attribute:: SAE_FETCHURL_HOST

   SAE服务端参数配置


:mod:`sae.util` -- Utilities辅助功能
-------------------------------------------------

.. module:: sae.util
   :synopsis: 

.. function:: get_signature(key, msg)

   签名算法

.. function:: get_signatured_headers(headers)

   对list格式的headers进些签名，返回dict格式的headers

   输入headers示例:  [('Content-type', 'text/plain'), ...]


:mod:`sae.urlfetch` -- fetchurl服务
-------------------------------------------------

.. module:: sae.urlfetch
   :synopsis: 

fetchurl检测已经嵌入到urllib2，一般情况下不需要直接使用该模块。

.. function:: wrap(req)

   封装req对象，设置fetchurl服务headers，返回一个新req对象
   
   如果req.host在可信主机列表中，直接返回原req


SAE服务
------------------
Mail, TaskQueue, Memcache, Storage等SAE服务封装模块会陆续提供。

http://sae.sina.com.cn/?m=devcenter&catId=33

