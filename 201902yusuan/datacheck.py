# -*- coding: utf-8 -*-
# @Time    : 2019/2/26 9:01
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : datacheck.py
# @Software: PyCharm


import pandas as pd
import json

path = r'D:\toone\项目案例\201902概预算\第二次\概预算'

with open(path + '\概预算.json', encoding='utf-8') as f:
    data = json.load(f)
    data = pd.DataFrame(data['RECORDS'])
    data.head(5000).to_excel(path + '\数据参考.xlsx')

