#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import csv
from itertools import islice
from sklearn.decomposition import PCA
from sklearn import metrics  # 评估模型
import sklearn.cluster as skc
import matplotlib.pyplot as plt


def MaxMinNormalization(x):
    """[0,1] normaliaztion"""
    x = (x - np.min(x)) / (np.max(x) - np.min(x))
    return x


def ParameterAdjustment(X):
    # 构建空列表，用于保存不同参数组合下的结果
    res = []
    # 迭代不同的eps值
    for eps in np.arange(0.001, 1, 0.05):
        # 迭代不同的min_samples值
        for min_samples in range(2, 10):
            dbscan = skc.DBSCAN(eps=eps, min_samples=min_samples)
            # 模型拟合
            dbscan.fit(X)
            # 统计各参数组合下的聚类个数（-1表示异常点）
            n_clusters = len([i for i in set(dbscan.labels_) if i != -1])
            # 异常点的个数
            outliners = np.sum(np.where(dbscan.labels_ == -1, 1, 0))
            # 统计每个簇的样本个数
            stats = str(pd.Series([i for i in dbscan.labels_ if i != -1]).value_counts().values)
            res.append({'eps': eps, 'min_samples': min_samples, 'n_clusters': n_clusters, 'outliners': outliners,
                        'stats': stats})
    # 将迭代后的结果存储到数据框中
    pd.set_option('display.max_rows', 160)
    pd.set_option('display.max_columns', 5)
    df = pd.DataFrame(res)
    # 根据条件筛选合理的参数组合
    df.loc[df.n_clusters == 3, :]
    return df


csv_file = csv.reader(open('Abnormal operation.csv', 'r'))
content = []
for line in islice(csv_file, 1, None):
    content.append(list(map(float, line[1:4])))
X = np.array(content)

print(X)
for i in range(3):
    X[:, i] = MaxMinNormalization(X[:, i])
pca = PCA(n_components='mle')
X = pca.fit_transform(X)
print(pca.explained_variance_ratio_)
db = skc.DBSCAN(eps=0.101, min_samples=9).fit(X)
labels = db.labels_

raito = len(labels[labels[:] == -1]) / len(labels)  #计算噪声点个数占总数的比例
print('噪声比:', format(raito, '.2%'))

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)  # 获取分簇的数目

print('分簇的数目: %d' % n_clusters_)
print("轮廓系数: %0.3f" % metrics.silhouette_score(X, labels)) #轮廓系数评价聚类的好坏

for i in range(n_clusters_):
    print('簇 ', i, '的所有样本:')
    one_cluster = X[labels == i]
    print(one_cluster)
    plt.plot(one_cluster[:,0],one_cluster[:,1],'o')

plt.show()
