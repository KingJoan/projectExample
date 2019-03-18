# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 16:52
# @Author  : Joan
# @Email   : sj11249187@126.com
# @File    : day02.py
# @Software: PyCharm

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

def iris_Kneighbors_demo():
    """
    KNN
    :return:
    """
    # 1. 获取数据
    iris = load_iris()
    # 2. 数据集划分
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, random_state=6)
    # 3. 特征工程,标准化
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test) # 与训练保持一致
    # 4. KNN预估器流程
    estimator = KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train, y_train)
    # 5. 模型评估
    y_predict = estimator.predict(x_test)
    print("直接比对真实值和预测值：\n", y_test == y_predict)
    print("计算准确率：\n", estimator.score(x_test, y_test))
    return None


if __name__ == "__main__":
    iris_Kneighbors_demo()