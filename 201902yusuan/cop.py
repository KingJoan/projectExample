# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 9:57
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : cop.py
# @Software: PyCharm


from PIL import Image
import pytesseract
#上面都是导包，只需要下面这一行就能实现图片文字识别
text=pytesseract.image_to_string(Image.open(r'HpsmnI873.jpg'),lang='chi_sim')
print(text)
