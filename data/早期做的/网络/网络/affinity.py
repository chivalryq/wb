import pandas as pd
from sklearn.cluster import KMeans, AffinityPropagation
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
af = AffinityPropagation(preference=-50).fit(X_principal)
labels = af.labels_
cluster_centers_indices = af.cluster_centers_indices_

print('Affinity propagation')
print('轮廓系数：'+str(silhouette_score(X_principal,labels)))
print('Calinski-Harabaz Index:'+str(calinski_harabasz_score(X_principal, labels)))
