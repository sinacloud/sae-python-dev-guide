# -*-coding: utf8 -*-

import urllib
import urllib2
from apibus_handler import APIBusHandler

ACCESSKEY = '你的某个开启了服务的应用的accesskey'
SECRETKEY = '你的某个开启了服务的应用的secretkey'

apibus_handler = APIBusHandler(ACCESSKEY, SECRETKEY)
opener = urllib2.build_opener(apibus_handler)

print 'call sae segment api:'
chinese_text = '中文文本'
url = 'http://segment.sae.sina.com.cn/urlclient.php?word_tag=1&encoding=UTF-8'
payload = urllib.urlencode([('context', chinese_text),])
print opener.open(url, payload).read()

# sending sms
print 'call sae sms api:'
url = 'http://inno.smsinter.sina.com.cn/sae_sms_service/sendsms.php'
payload = 'mobile=186****8203&msg=helloworld'
print opener.open(url, payload).read()
