import pandas as pd
import numpy as np
import sklearn.cluster
import sklearn.metrics
from sklearn.cluster import KMeans,AffinityPropagation,MeanShift,SpectralClustering
from sklearn.metrics import silhouette_score,calinski_harabasz_score
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
    #绘制kmeans肘部图
    #param X 数据集
    ss=[]
    chs=[]
    SSE=[]
    for k in range(2,10):
        kmeans_model = KMeans(n_clusters=k, random_state=1).fit(X)
        labels = kmeans_model.labels_
        points=print_score(X,labels)
        SSE.append(kmeans_model.inertia_)
        ss.append(points[0])
        chs.append(points[1])
    
    x = range(2,10)
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(x,SSE,'o-')
    plt.show()

def main():
    file=r'C:\Users\jnjga\OneDrive - business\桌面\university\服创\data\企业诚信度\honesty.csv'

    X_raw=pd.read_csv(file)
    X_before=X_raw.loc[:,['is_justice_creditaic','is_justice_credit','nega_is_kcont']]
    #print(X)

    X=pd.DataFrame(scale(X_before),columns=['is_justice_creditaic','is_justice_credit','nega_is_kcont']) #标准化
    
    X=X.loc[:,['is_justice_creditaic','is_justice_credit','nega_is_kcont']]
    #X.to_csv('test_scale.csv')
    #kmeans_model = KMeans(n_clusters=4, random_state=1).fit(X)
    #ap_model=AffinityPropagation(damping=0.5, max_iter=500).fit(X)
    ms_model=MeanShift(bandwidth=1.9).fit(X)
    #sc_model=SpectralClustering(n_clusters=5).fit(X)

    labels = ms_model.labels_
    
    print(set(ms_model.labels_))
    print_score(X,labels,_print=False)
    labels_df = pd.DataFrame(labels,columns=['labels'])
    new_df=pd.concat([X_raw,labels_df],axis=1)
    print(new_df.info())
    file=r'C:\Users\jnjga\OneDrive - business\桌面\university\服创\data\企业诚信度\new2.csv'
    new_df.to_csv(file)


    
    #画分类效果图
    fig = plt.figure()
    ax = Axes3D(fig)

    
    
    colours = ['red', 'green', 'blue','black','purple','orange','lime','pink','cyan','olive']
    colours[-1] = 'k'

    
    cvec = [colours[label] for label in labels]

    ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('X', fontdict={'size': 15, 'color': 'red'})
    ax.scatter(X['is_justice_creditaic'], X['is_justice_credit'], X['nega_is_kcont'], c=cvec, label='点')

    
    plt.show()
    
    
if __name__ == "__main__":
    main()