import pandas as pd
from numpy import unique
from sklearn.cluster import Birch
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize

X = pd.read_csv('triple.csv')
print(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_normalized = normalize(X_scaled)
X_normalized = pd.DataFrame(X_normalized)

X_principal = X_normalized
X_principal.columns = ['P1', 'P2', 'P3']

cluster = Birch(n_clusters=None).fit(X_principal)
labels = cluster.labels_

print('Birch Clustering')
print("number of estimated clusters : %d" % len(unique(labels)))
print('轮廓系数：' + str(silhouette_score(X_principal, labels)))
print('Calinski-Harabaz Index:' + str(calinski_harabasz_score(X_principal, labels)))
