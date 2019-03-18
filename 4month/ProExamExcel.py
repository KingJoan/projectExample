# -*- coding: utf-8 -*-
# @Time    : 2018/5/10 13:34
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : ProExamExcel.py
# @Software: PyCharm
# @Version : python 2.7


import numpy as np


def handle_data(data):
    # 差值取索引位置  连续值最后一个
    pos, = np.where(np.diff(data.zmKind))
    # 位置转为二维数组
    l = len(pos)
    if l % 2 != 0:
        pos = pos[:-1]
    pos_array = pos.reshape(l/2, 2)
    # 以转为字典 键：清单索引 值：定额索引
    d = {} # 清单索引-定额索引
    for i in range(len(pos_array)):
        d[pos_array[i][0]] = pos_array[i][1]

    # 定额补齐  键：清单索引  值：定额索引
    for k,v in d.items():
        if v-k>1:
            d[k] = list(range(k+1,v+1))

    dqn = {}  # 清单索引-定额编号
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
    for k, v in dnq.items():
        if len(v) > 1:
            qdsy.append(dnq[k])
    return data, d, qdsy


def return_qd_no(qdsy_ever,data):

    # 定义lambda函数：索引减1
    f = lambda x: x - 1

    unitPrices = []
    qds = []
    for qd in qdsy_ever:
        qdup = qd
        qdno = data.ix[qd, 'no']

        # qdno = qdno.encode('utf-8',errors='ignore')
        qdupno = data.ix[qdup,'no']
        no = []
        if type(qdno) != float and qdno.startswith('-'):

            n = data.ix[qd, 'level'] - data.ix[qdup, 'level']
            while n < 1 or (n < 2 and type(qdupno) != float and qdupno.startswith('-')):

                qdup = f(qdup)

                n = data.ix[qd, 'level'] - data.ix[qdup, 'level']
                if n == 1 or n == 2:
                    qdupno = data.loc[qdup, 'no']
                    no.append(qdupno)
            if len(no) >1:
                s = no[-1]  + no[0] + qdno
            else:
                s = no[0] + qdno
        else:
            s = data.ix[qd,'no']
        workSpale = data.ix[qd,'workSpale']
        roadLevel = data.ix[qd,'roadLevel']
        name = data.ix[qd,'name']
        costfileName = data.ix[qd,'costfileName']
        editTime = data.ix[qd,'editTime']
        unitPrice = data.ix[qd,'unitPrice']
        unit = data.ix[qd,'unit']
        qd = [s,name,unit,unitPrice,costfileName,editTime,workSpale,roadLevel]
        qds.append(qd)
        unitPrices.append(unitPrice)

    # 计算同一类型的清单项的综合单价区间 [min,max]

    unitPrices = set(unitPrices)
    if len(unitPrices) >1:
        unitPrice_section = '[' + str(min(unitPrices)) + ',' + str(max(unitPrices))+ ']'
    elif len(unitPrices) == 1:
        unitPrice_section = unitPrices.pop()
    else:
        unitPrice_section = None
    return qds,unitPrice_section


def return_de_no(qdsy_ever,d,data):

    des = d[qdsy_ever[0]]
    de = []
    if type(des) == np.int64:
        deno = data.ix[des,'no']
        deunit = data.ix[des,'unit']
        dename = data.ix[des,'name']
        decostfileName = data.ix[des,'costfileName']
        deeditTime = data.ix[des,'editTime']
        deworkSpale = data.ix[des, 'workSpale']
        deroadLevel = data.ix[des, 'roadLevel']
        e = [deno,dename,deunit,u'--',decostfileName,deeditTime,deworkSpale,deroadLevel]
        de.append(e)
    else:
        for i in des:
            deno = data.ix[i, 'no']
            deunit = data.ix[i, 'unit']
            dename = data.ix[i, 'name']
            decostfileName = data.ix[i, 'costfileName']
            deeditTime = data.ix[i, 'editTime']
            deworkSpale = data.ix[i, 'workSpale']
            deroadLevel = data.ix[i, 'roadLevel']
            e = [deno,dename,deunit,u'--',decostfileName,deeditTime,deworkSpale,deroadLevel]
            de.append(e)

    return de





