# -*- coding: utf-8 -*-
# @Time    : 2018/5/10 14:43
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : excel_to.py
# @Software: PyCharm
# @Version : python 2.7

import xlwt
from ProExamExcel import *
import pandas as pd


path = r'F:\toone\实习\实习4月\项目案例\数据\一般公路二级.xlsx'

to_path = r'F:\toone\实习\实习4月\项目案例\结果\一般二级公路.xls'
# 读取数据

workbook = xlwt.Workbook(to_path)

datas = pd.read_excel(path)

province = set(datas['workSpale'])


for i in province:
    data = datas[datas.workSpale == i]
    data = data.reset_index(drop=True)
    sheet = workbook.add_sheet(i)
    data, d, qdsy = handle_data(data)
    ll = 1
    title = [u"编号", u"名称", u"单位", u"单价", u"造价文件", u"编制时间",u"地区",u"公路等级"]
    for i in range(8):
        sheet.write(0,i+1,title[i])

    for j in range(len(qdsy)):
        qdsy_ever = qdsy[j]

        qd,unitPrice_section = return_qd_no(qdsy_ever,data)
        de = return_de_no(qdsy_ever, d, data)

        lqd = len(qd)
        lde = len(de)

        sheet.write(ll, 0, u"清单项")
        for j in range(lqd):
            for k in range(8):
                sheet.write(ll + j, k + 1, qd[j][k])

        sheet.write(ll + lqd, 0, u"定额项")

        for x in range(lde):
            for e in range(8):

                sheet.write(ll + x + lqd, e + 1, de[x][e])

        sheet.write(ll + lqd + lde, 0, u"综合单价区间")
        sheet.write(ll + lqd + lde, 1, unitPrice_section)
        ll = ll + lqd + lde + 1

workbook.save(to_path)
