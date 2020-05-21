import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from numpy import unique

X = pd.read_csv('triple.csv')
X.fillna(method='ffill', inplace=True)
print(X.head())
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_normalized = normalize(X_scaled)
X_normalized = pd.DataFrame(X_normalized)
'''
pca = PCA(n_components=3)
X_principal = pca.fit_transform(X_normalized)
X_principal = pd.DataFrame(X_principal)
X_principal.columns = ['P1', 'P2']
print(X_principal.head())
'''
X_principal = X_normalized
X_principal.columns = ['P1', 'P2', 'P3']
db_default = DBSCAN(eps=0.5, min_samples=2000).fit(X_principal)
labels = db_default.labels_

print('DBSCAN：')
print("number of estimated clusters : %d" % len(unique(labels)))
print('轮廓系数：' + str(silhouette_score(X_principal, labels)))
print('Calinski-Harabaz Index:' + str(calinski_harabasz_score(X_principal, labels)))

colours = ['r', 'g', 'b', 'c', 'm']
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

labels = db_default.labels_

ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'red'})
ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'red'})
ax.set_xlabel('X', fontdict={'size': 15, 'color': 'red'})
ax.scatter(X_principal['P1'], X_principal['P2'], X_principal['P3'], c=cvec, label='点')

# plt.legend((r, g, b, k), ('Label 0', 'Label 1', 'Label 2', 'Label -1'))
plt.show()
