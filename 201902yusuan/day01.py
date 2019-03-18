# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 15:59
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : day01.py
# @Software: PyCharm
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def datasets_demo():
    """
    sklearn数据集使用
    :return:
    """
    # 获取数据集
    iris = load_iris()
    print("鸢尾花数据集：\n",iris)
    print("鸢尾花数据集描述：\n",iris['DESCR'])
    print("查看特征值的名字：\n",iris.feature_names)
    print("查看特征值：\n",iris.data,iris.data.shape)

    # 数据集划分
    x_train,x_test,y_train,y_test = train_test_split(iris.data,iris.target,test_size=0.2,random_state=22)
    print("训练集的特征值：\n",x_train,x_train.shape)
    return None

def dict_demo():
    '''
    字典特征抽取
    :return:
    '''
    data = [{'city': '北京', 'temperature': 100}, {'city': '上海', 'temperature':60}, {'city':'深圳', 'temperature':30}]
    # 1. 实例化一个转化器
    transfer = DictVectorizer(sparse=False)
    # 2. 调用fit_transform()
    data_new = transfer.fit_transform(data)
    data_feature = transfer.get_feature_names()
    print(data_new)
    print("特征名字：", data_feature)

    return None

def text_demo():
    """
    文本特征提取CountVectorizer
    :return:
    """
    data = ["Life is short,i like like python","life is too long,i dislike python"]
    # 1. 实例化一个转换器类
    transfer = CountVectorizer()
    # 2. 调用fit_transform
    data_new = transfer.fit_transform(data)
    print("data_new:\n",data_new.toarray())
    print("特征名字：\n", transfer.get_feature_names())
    return None

def chinese_text_demo():
    """
    中文文本特征抽取：CountVectorizer
    :return:
    """
    data = ["我 爱 北京 天安门", "我 爱看 北京 天安门 升国旗"]
    # 1. 实例化一个转换类
    transfer = CountVectorizer()
    # 2. 调用fit_tansform
    data_new = transfer.fit_transform(data)
    print("data_new:\n",data_new)
    print("特征名字：\n", transfer.get_feature_names())
    return None

def cut_word(text):
    """
    中文分词：“我爱北京天安门” >> “我 爱 北京 天安门”
    :param text:
    :return:
    """
    return ' '.join(list(jieba.cut(text)))
def chinese_test_demo2():
    """
    中文文本抽取，自动分词
    :return:
    """
    data = ["段氏香的代表律师团于当天向总检察署提呈陈情书，要求同样撤销段氏香的谋杀罪状。段氏香于今早8时30分，"
            "戴上红色头巾及身穿马来传统服装，在特警护送下抵达法庭。", "2017年2月13日，一名朝鲜籍男子在吉隆坡国际"
                                           "机场寻求医疗救助，随后在送往医院途中身亡。马来西亚警方称，死者面部和眼"
                                           "部均含有VX神经性毒剂。马来西亚警察总长之后确认，在吉隆坡国际机场遇袭身"
                                           "亡的朝鲜籍男子为金正男。"]
    data_new = []
    for sent in data:
        data_new.append(cut_word(sent))

    transfer = CountVectorizer(stop_words=['之后','同样','随后'])
    data_final = transfer.fit_transform(data_new)
    print("data_final:\n",data_final.toarray())
    print("特征名字：\n",transfer.get_feature_names())
    return None

def tfidf_demo():
    """
    用户TF-IDF的方法进行文本特征抽取
    :return:
    """
    data = ["段氏香的代表律师团于当天向总检察署提呈陈情书，要求同样撤销段氏香的谋杀罪状。段氏香于今早8时30分，"
            "戴上红色头巾及身穿马来传统服装，在特警护送下抵达法庭。", "2017年2月13日，一名朝鲜籍男子在吉隆坡国际"
                                           "机场寻求医疗救助，随后在送往医院途中身亡。马来西亚警方称，死者面部和眼"
                                           "部均含有VX神经性毒剂。马来西亚警察总长之后确认，在吉隆坡国际机场遇袭身"
                                           "亡的朝鲜籍男子为金正男。"]
    data_new = []
    for sent in data:
        data_new.append(cut_word(sent))
    # 1. 实例化一个转换器
    transfer = TfidfVectorizer(stop_words=['之后','同样','随后'])
    # 2. 调用fit_transform
    data_final = transfer.fit_transform(data_new)
    print("data_final:\n",data_final.toarray())
    print("特征名字：\n",transfer.get_feature_names())

    return None

def minmax_demo():
    """
    归一化
    :return:
    """
    # 1. 获取数据
    data = pd.read_csv('dating.txt')
    print("data:\n", data)
    data = data.iloc[:, :3]
    # 2. 实例化MinMaxScalar
    scalar = MinMaxScaler(feature_range=(2,3))
    # 3. 通过fit_transform转换
    data_new = scalar.fit_transform(data)
    print("data_new:\n", data_new)
    return None

def stand_demo():
    """
    标准化
    :return:
    """
    # 1. 获取数据
    data = pd.read_csv('dating.txt')
    data = data.iloc[:,:3]
    # 2. 实例化一个转换器类
    stand = StandardScaler()
    # 3. 调用fit_transform
    data_new = stand.fit_transform(data)
    print("data_new: \n", data_new)
    return None

def pca_demo():
    """
    pca降维
    :return:
    """
    data = [[2,8,4,5],[6,3,0,0],[5,4,9,1]]
    # 1. 实例化一个转换器类
    transfer = PCA(n_components=0.95)
    # 2. 调用transform
    data_new = transfer.fit_transform(data)
    print("data_new:\n",data_new)
    return None

if __name__ == "__main__":
    # datasets_demo()
    # dict_demo()
    # text_demo()
    # chinese_text_demo()
    # print(cut_word("我爱北京天安门"))
    # chinese_test_demo2()
    # tfidf_demo()
    # minmax_demo()
    # stand_demo()
    pca_demo()

