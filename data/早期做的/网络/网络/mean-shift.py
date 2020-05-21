import pandas as pd
from sklearn.cluster import estimate_bandwidth, MeanShift
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize

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
# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(X_principal, quantile=0.2, n_samples=500)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X_principal)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = pd.np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

print('Mean-shift')
print(ms.bandwidth)
print('轮廓系数：'+str(silhouette_score(X_principal,labels)))
print('Calinski-Harabaz Index:'+str(calinski_harabasz_score(X_principal, labels)))
