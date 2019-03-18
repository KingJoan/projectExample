# -*- coding: utf-8 -*-
# @Time    : 2018/4/28 14:56
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : loaddata.py
# @Software: PyCharm
# @Version : python 2.7
'''项目案例分析'''


import json
from pandas.io.json import json_normalize
import pandas as pd

# 加载数据
path = r'F:\toone\实习\实习4月\项目案例\项目案例.json'
f = open(path).read()
data = json.loads(f)
df = json_normalize(data)

writer = pd.ExcelWriter('data.xlsx')
df.to_excel(writer,'sheet1')
writer.save()
