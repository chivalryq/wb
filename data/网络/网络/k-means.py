import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA

def print_score(X,labels,_print=True):
    #打印评分,返回这两个评分的二元组
    #param X 数据集
    #param _print 为True时打印两个值，默认打印
    #param labels 与数据集等长的标签
    #return 一个两个分数组成的二元组
    a=silhouette_score(X, labels, metric='euclidean')
    b=calinski_harabasz_score(X,labels)
    print("轮廓系数为",end='')
    print(a)
    print('Calinski-Harabasz指数为',end='')
    print(b)
    return (a,b)

def run_kmeans(X):
    # 绘制kmeans肘部图
    # param X 数据集
    ss = []
    chs = []
    SSE = []
    for k in range(2, 10):
        kmeans_model = KMeans(n_clusters=k, random_state=1).fit(X)
        labels = kmeans_model.labels_
        points = print_score(X, labels)
        SSE.append(kmeans_model.inertia_)
        ss.append(points[0])
        chs.append(points[1])

    x = range(2, 10)
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(x, SSE, 'o-')
    plt.show()

X = pd.read_csv('triple.csv')
print(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_normalized = normalize(X_scaled)
X_normalized = pd.DataFrame(X_normalized)
'''
pca = PCA(n_components=3)
X_principal = pca.fit_transform(X_normalized)
X_principal = pd.DataFrame(X_principal)
X_principal.columns = ['P1', 'P2','P3']
print(X_principal.head())
'''
X_principal = X_normalized
X_principal.columns = ['P1', 'P2', 'P3']
k_default = KMeans(n_clusters=4).fit(X_principal)
labels = k_default.labels_

print('K-Means, n_clusters=4')
print('轮廓系数：'+str(silhouette_score(X_principal,labels)))
print('Calinski-Harabaz Index:'+str(calinski_harabasz_score(X_principal, labels)))


colours = ['r', 'g', 'b', 'c', 'b']
colours[-1] = 'k'

cvec = [colours[label] for label in labels]

'''
r = plt.scatter(X_principal['P1'], X_principal['P2'], color='r')
g = plt.scatter(X_principal['P1'], X_principal['P2'], color='g')
b = plt.scatter(X_principal['P1'], X_principal['P2'], color='b')
k = plt.scatter(X_principal['P1'], X_principal['P2'], color='k')

plt.figure(figsize=(9, 9))
plt.scatter(X_principal['P1'], X_principal['P2'], c=cvec)
plt.legend((r, g, b, k), ('Label 0', 'Label 1', 'Label 2', 'Label -1'))
plt.show()
'''

fig = plt.figure()
ax = Axes3D(fig)

labels = k_default.labels_

colours = ['r', 'g', 'b', 'c']
colours[-1] = 'k'

cvec = [colours[label] for label in labels]

ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'red'})
ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'red'})
ax.set_xlabel('X', fontdict={'size': 15, 'color': 'red'})
ax.scatter(X_principal['P1'], X_principal['P2'], X_principal['P3'], c=cvec, label='点')

# plt.legend((r, g, b, k), ('Label 0', 'Label 1', 'Label 2', 'Label -1'))
plt.show()
