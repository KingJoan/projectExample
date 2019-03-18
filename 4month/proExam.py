# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 13:34
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : premanage.py
# @Software: PyCharm
# @Version : python 2.7


import numpy as np
import codecs



def handle_data(data):
    # 差值取索引位置  连续值最后一个
    pos, = np.where(np.diff(data.zmKind))
    # 位置转为二维数组
    l = len(pos)
    if l % 2 != 0:
        pos = pos[:-1]
    pos_array = pos.reshape(l/2,2)
    # 以转为字典 键：清单索引 值：定额索引
    d = {} # 清单索引-定额索引
    for i in range(len(pos_array)):
        d[pos_array[i][0]] = pos_array[i][1]

    # 定额补齐  键：清单索引  值：定额索引
    for k,v in d.items():
        if v-k>1:
            d[k] = list(range(k+1,v+1))

    dqn = {} # 清单索引-定额编号
    # 键：清单索引 值：定额编号
    for k,v in d.items():
        dqn[k] = data.ix[v,'no']


    # 键：定额编号 值：清单索引
    dnq = {}  # 定额编号-清单索引 字典
    for k,v in dqn.items():
        if type(v) == int:
            dnq.setdefault(v, []).append(k)
        else:
            dnq.setdefault(tuple(v),[]).append(k)


    # 套用相同定额的清单索引
    qdsy = [] # 清单索引 列表
    for k,v in dnq.items():
        if len(v)>1:
            qdsy.append(dnq[k])
    return data,d,qdsy



# qdsy列表中的每一个子列表为同一类型的清单项或工艺
# 最终结果输出中的形式为： xxx清单（清单编号）


def return_qd_no(qdsy_ever,data):

    # 定义lambda函数：索引减1
    f = lambda x: x - 1

    unitPrice = []
    qd_nos = []
    unitPrice_section = None
    for qd in qdsy_ever:
        qdup = qd
        qdno = data.ix[qd, 'no']

        # qdno = qdno.encode('utf-8',errors='ignore')
        qdupno = data.ix[qdup,'no']
        no = []
        if type(qdno) != float and qdno.startswith('-') :

            n = data.ix[qd, 'level'] - data.ix[qdup, 'level']
            # 清单索引逐个减1，直到level-1
            # while data.ix[qdup,'level']>= data.ix[qd,'level'] or (type(data.ix[qdup,'no']) != float and qdupno.startwith('-')):
            #     qdup = f(qdup)
            #
            #     qdupno = data.ix[qdup,'no']
            #     s.append(qdupno)
            #     if data.ix[qd,'level'] - data.ix[qdup,'level'] >= 1 :
            #
            #         qd_no = u'\t名称：' + data.ix[qd,'name'] + u'\t编号：(' + str(data.ix[qdup,'no']) + str(data.ix[qd,'no']) + u')\n'
            #         qd_no = qd_no.encode('gb2312',errors='ignore')
            #         qd_nos.append(qd_no)
            while n < 1 or (n < 2 and type(qdupno) != float and qdupno.startswith('-')):

                qdup = f(qdup)

                n = data.ix[qd, 'level'] - data.ix[qdup, 'level']
                if n == 1 or n == 2:
                    qdupno = data.loc[qdup, 'no']
                    no.append(qdupno)
            if len(no) >1:
                s = str(no[-1])  + str(no[0]) + qdno
            else:
                if type(no[0]) == float:
                    n = str(no[0])
                else:
                    n = no[0].encode('utf-8',errors='ignore')
                s = n + qdno.encode('utf-8','ignore')
                s = unicode(s,'utf-8','ignore')

            qd_no = u'\t名称：' + str(data.ix[qd,'name']) + u'\t造价文件：' + str(data.ix[qd,'costfileName']) + u'\t编制时间：' + str(data.ix[qd,'editTime'])  + u'\t编号：(' + s + u')\n'
            # qd_no = qd_no.encode('utf-8',errors='ignore')
            qd_nos.append(qd_no)
        else:
            dno = data.ix[qd,'no']
            if type(dno) == float:
                dno = str(dno)
            name = data.ix[qd,'name'].encode('utf-8','ignore')
            cost = data.ix[qd,'costfileName'].encode('utf-8','ignore')
            time = data.ix[qd,'editTime'].encode('utf-8','ignore')
            dno = dno.encode('utf-8','ignore')
            qd_no = u'\t名称：' + name + u'\t造价文件：' + cost + u'\t编制时间：' + time + u'\t编号：(' + dno + u')\n'
            # qd_no = qd_no.encode('utf-8',errors='ignore')
            qd_nos.append(qd_no)

        unitPrice.append(data.ix[qd,'unitPrice'])
    # 计算同一类型的清单项的综合单价区间 [min,max]

    unitPrice = set(unitPrice)
    if len(unitPrice) >1:
        unitPrice_section = '[' + str(min(unitPrice)) + ',' + str(max(unitPrice)) + ']\n'
    elif len(unitPrice) == 1:
        unitPrice_section = str(unitPrice.pop()) + '\n'
    else:
        unitPrice_section = None
    return qd_nos,unitPrice_section

# 格式化输出
'''
高速公路广东省XX清单项，所属造价文件：，其编制时间为：综合单价区间：，套取的定额编号和名称单位是什么
'''
def write(qdsy_ever,d,data,path):
    f = codecs.open(path,'a','utf-8',errors='ignore')
    qds = data.ix[qdsy_ever[0],'workSpale'] + data.ix[qdsy_ever[0],'roadLevel'] + u"清单项：\n"
    zhup = u"综合单间区间为："
    des = u"所套定额:" + u'\n'
    qd_nos,unitPrice_section = return_qd_no(qdsy_ever,data)
    f.write(u'\n\n')
    f.write(qds)


    for i in qd_nos:
        # i = i.encode('utf-8',errors='ignore')
        # i = unicode(i,'utf-8',errors='ignore')
        f.write(i)
    f.write(zhup  + unitPrice_section)

    f.write(des)


    if type(d[qdsy_ever[0]]) == np.int64:
        qno = data.ix[d[qdsy_ever[0]],'no']
        unit = data.ix[d[qdsy_ever[0]],'unit']
        if type(qno) == float or type(qno) == int:
            qno = str(qno)
        if type(unit) == float:
            unit = str(unit)
        de = u"\t名称：" + data.ix[d[qdsy_ever[0]],'name'] + u'\t编号:(' + qno + u"）\t单位：" + unit +u'\n'
        # de = de.encode('utf-8',errors='ignore')
        f.write(de)

    else:
        for i in d[qdsy_ever[0]]:
            ino = data.ix[i, 'no']
            if type(ino) == float or type(ino) == int:
                ino = str(ino)
            de = u"\t名称：" + data.ix[i,'name'] + u"\t编号：(" + ino + u"）\t单位：" + data.ix[i,'unit'] + u'\n'
            # de = unicode(de,'utf-8',errors='ignore')
            f.write(de)

    f.write(u'\n')
    f.close()
