# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 10:46
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : read_print.py
# @Software: PyCharm
# @Version : python 2.7

from proExam import *
import pandas as pd
path = r'F:\toone\实习\实习4月\项目案例\数据\一级公路.xlsx'

path2 = r'F:\toone\实习\实习4月\项目案例\数据\一级公路.doc'

# 读取数据
datas = pd.read_excel(path)

province = set(datas['workSpale'])


for i in province:
    data = datas[datas.workSpale == i]
    data = data.reset_index(drop=True)

    data, d, qdsy = handle_data(data)
    for i in range(len(qdsy)):
        qdsy_ever = qdsy[i]
        write(qdsy_ever, d, data, path2)
