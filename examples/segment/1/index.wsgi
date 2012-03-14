#-*-coding: utf8 -*-

"""
分词服务请求
------------

SAE分词服务请求采用以下形式的HTTP网址： ::

    http://segment.sae.sina.com.cn/urlclient.php?parameters

parameters为请求参数，多个参数之间使用&分割，以下列出了这些参数和其可能的值。

* word_tag: 是否返回词性数据。0表示不返回，1表示返回，默认为0不返回。
* encoding: 请求分词的文本的编码，可以为: GB18030、UTF-8、UCS-2，默认为UTF-8。

请求分词的文本以post的形式提交。

* context: 请求分词的文本。目前限制文本大小最大为10KB。

分词服务响应
------------

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
"""

import sae
import urllib
import urllib2

_SEGMENT_BASE_URL = 'http://segment.sae.sina.com.cn/urlclient.php'

some_chinese_text = """
采莲赋 （萧绎 ）
紫茎兮文波，红莲兮芰荷。绿房兮翠盖，素实兮黄螺。于时妖童媛女，荡舟心许，
（益鸟，音益）首徐回，兼传羽杯。棹将移而藻挂，船欲动而萍开。尔其纤腰束
素，迁延顾步。夏始春余，叶嫩花初。恐沾裳而浅笑，畏倾船而敛裾，故以水溅
兰桡，芦侵罗（衤荐，音间）。菊泽未反，梧台迥见，荇湿沾衫，菱长绕钏。泛
柏舟而容与，歌采莲于江渚。歌曰：“碧玉小家女，来嫁汝南王。莲花乱脸色，
荷叶杂衣香。因持荐君子，愿袭芙蓉裳。”
"""

def segment(text):
    payload = urllib.urlencode([('context', text),])
    args = urllib.urlencode([('word_tag', 1), ('encoding', 'UTF-8'),])
    url = _SEGMENT_BASE_URL + '?' + args
    return urllib2.urlopen(url, payload).read()

def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)

    output = segment(some_chinese_text)

    return [output]

application = sae.create_wsgi_app(app)
