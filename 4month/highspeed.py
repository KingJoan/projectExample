# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 16:18
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : highspeed.py
# @Software: PyCharm
# @Version : python 2.7

import pandas as pd

path = r'F:\toone\实习\实习4月\项目案例\数据\高速公路.xlsx'

path1 = r'F:\toone\实习\实习4月\项目案例\数据\高速公路15.xlsx'

path2 = r'F:\toone\实习\实习4月\项目案例\数据\高速公路16.xlsx'

df = pd.read_excel(path)

provinces = list(set(df['workSpale']))
province = provinces[:15]
df1 = df.loc[df['workSpale'].isin(province)]

df2 = df.loc[~df['workSpale'].isin(province)]

writer1 = pd.ExcelWriter(path1)
df1.to_excel(writer1,'Sheet1')
writer1.save()

writer2 = pd.ExcelWriter(path2)
df2.to_excel(writer2,'Sheet1')
writer2.save()



