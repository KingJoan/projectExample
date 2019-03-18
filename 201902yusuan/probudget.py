# -*- coding: utf-8 -*-
# @Time    : 2019/2/26 14:43
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : probudget.py
# @Software: PyCharm

import numpy as np
import json
import pandas as pd
import time


def readJson(path, filename):
    with open(path + '\\' + filename, encoding='utf-8') as f:
        data = json.load(f)
        data = pd.DataFrame(data['RECORDS'])
        return data


def qd_de_mix(df):
    '''
    将项（索引）与所套定额（索引）绑定在一起，项为键，定额为值
    :param df: 项目案例数据dataframe格式，且只留项与定额
    :return:
    '''
    # 求zmkind 差值,zmkind中10-定额；50-项，项
    zmKind_diff = np.diff(df.zmKind)
    # 取连续值的最后一个的索引
    pos, = np.where(zmKind_diff)
    # 如果差值最后一位等于0,则索引pos最后增加zmKind最后一位的索引
    if (len(zmKind_diff) > 1) and (zmKind_diff[-1] == 0):
        pos = np.append(pos, len(df.zmKind)-1)
    # 将索引pos转换为nx2的数组,[i][0]表示项,[i][1]表示定额
    if len(pos) % 2 != 0:
        pos = pos[:-1]
    pos_array = pos.reshape(len(pos)//2, 2)
    # 将数组转换为字典：键：项(连续项的最后一项)索引，值：定额（连续定额的最后一项）索引
    qd_de_last = {}
    for i in range(len(pos_array)):
        qd_de_last[pos_array[i][0]] = pos_array[i][1]
    # 定额索引补齐: 键：项索引，值：项所套全部定额索引
    qd_de_defill = {}
    for qd, de in qd_de_last.items():
        if de - qd > 1:
            qd_de_defill[qd] = list(range(qd+1, de+1))
        else:
            qd_de_defill[qd] = [de]

    return qd_de_defill


def qd_no_fill(df, qd_no_defill):
    '''
    项编号补齐
    :return:
    '''
    # 清单索引减一函数
    sub = lambda x: x-1

    for qdsy in qd_no_defill.keys():
        # qdsyup临时存放清单索引值以便于向上索引，初始值置为当前清单索引
        qdsyup = qdsy
        # 当前清单编号
        qdno = df.loc[qdsy, 'no']
        # 上一级清单编号,初始值置为当前清单编号
        no = [str(qdno)]
        n = df.loc[qdsy, 'level']
        while n > 1:
            qdsyup = sub(qdsyup)
            qdupl = df.loc[qdsyup, 'level']
            if qdupl < n:
                n -= 1
                if (qdupl == n) and (df.loc[qdsyup, 'zmKind'] != 10 ):
                    no.append(str(df.loc[qdsyup, 'no']))
        nofill = no[::-1]
        if len(nofill) == 0:
            df.loc[qdsy, 'nofill'] = ''
        else:
            df.loc[qdsy, 'nofill'] = '-'.join(nofill)
    return df


def same_qd(df, qd_de_defill):
    '''
    相同项所套定额
    :param df:
    :param qd_de_defill: 项索引--套用的定额索引字典
    :return: dataframe
    '''
    returnData = pd.DataFrame([], columns=['no', 'name', 'mark', 'unit', 'unitPrice',
                                           'costfileName', 'editTime', 'roadLevel', 'workSpale'])
    # 键：项索引 值：项name
    qd_name = {}
    for qdsy in qd_de_defill.keys():
        qd_name[qdsy] = df.loc[qdsy, 'name']
    # 键：项name 值：项索引   相同项名-项索引
    name_qd = {}
    for qdsy, name in qd_name.items():
        name_qd.setdefault(name, []).append(qdsy)

    # 键：项索引，值：定额编号
    qdsy_deno = {}
    for k, v in qd_de_defill.items():
        qdsy_deno[k] = []
        for vi in v:
            qdsy_deno[k].append(df.loc[vi, 'no'])
    # 键：定额编号 值：相同定额的项索引列表
    deno_qdsylist = {}
    for k, v in qdsy_deno.items():
        deno_qdsylist.setdefault(tuple(v), []).append(k)
    # 去除相同定额 键：项name 值：项索引
    qdname_qdsy = {}
    for kname, vqdsy in name_qd.items():
        qdname_qdsy[kname] = []
        for v in deno_qdsylist.values():
            if set(vqdsy) & set(v):
                if len(v) > 1:
                    vs = []
                    for vi in v:
                        if df.loc[vi, 'name'] == kname:
                            vs.append(vi)
                    qdname_qdsy[kname].append(vs[0])
                else:
                    qdname_qdsy[kname].extend(v)

    # 对每一个sameqdname 查找对应的qdsy
    for qdname in qdname_qdsy.keys():
        # 对每一个qdname查找对应qdsy列表
        qdsylist = qdname_qdsy[qdname]
        for i in range(len(qdsylist)):
            qdsy = qdsylist[i]
            desys = qd_de_defill[qdsy]
            qd = [df.loc[qdsy, 'nofill'], df.loc[qdsy, 'name'],  df.loc[qdsy, 'mark'], df.loc[qdsy, 'unit'], df.loc[qdsy, 'unitPrice'],
                  df.loc[qdsy, 'costfileName'], df.loc[qdsy, 'editTime'], df.loc[qdsy, 'roadLevel'],
                  df.loc[qdsy, 'workSpale']]
            returnData.loc[str(qdname) + '@项%d' % (i + 1), :] = qd

            for j in range(len(desys)):
                desy = desys[j]
                de = [df.loc[desy, 'no'], df.loc[desy, 'name'], df.loc[desy, 'mark'], df.loc[desy, 'unit'], df.loc[desy, 'unitPrice'],
                      df.loc[desy, 'costfileName'], df.loc[desy, 'editTime'], df.loc[desy, 'roadLevel'],
                      df.loc[desy, 'workSpale']]
                returnData.loc[str(qdname) + '@项%d套定额%d' % (i + 1, j + 1), :] = de

    return returnData


if __name__ == '__main__':
    path = r'D:\toone\项目案例\201902概预算\第二次\概预算'
    to_path = r'D:\toone\项目案例\201902概预算\第二次\概预算\结果v2'
    data = readJson(path, '概预算.json')
    data.loc[data['mark'] == "计算项", 'zmKind'] = 10
    print('程序执行开始时间：%s' % time.asctime())
    # data.head(2000).to_excel(to_path + '\data.xlsx')
    data = data[data['costfileName'].str.contains('预')]
    data = data[data['zmKind'].isin([10, 50])]
    data['name'].fillna('', inplace=True)
    data['roadLevel'].fillna('空', inplace=True)
    data['workSpale'].fillna('空', inplace=True)

    for m in list(set(data['roadLevel'])):
        writer = pd.ExcelWriter(to_path + '\%s.xlsx' % m, engine='openpyxl')
        for n in list(set(data['workSpale'])):
            datadf = data[(data['roadLevel'] == m) & (data['workSpale'] == n)]
            if datadf.empty:
                continue
            else:
                df = datadf.reset_index()
                qddefill = qd_de_mix(df)
                qdnofill = qd_no_fill(df, qddefill)
                result = same_qd(qdnofill, qddefill)
                result.to_excel(writer, sheet_name='%s' % n)
        writer.close()
    print('程序执行完成时间：%s' % time.asctime())


