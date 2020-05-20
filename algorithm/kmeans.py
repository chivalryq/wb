import sys
import pandas as pd
import numpy as np
import sklearn.datasets as sld 
import sklearn.cluster as slc
from sklearn.metrics import silhouette_score as skl_silScore
from sklearn.metrics import calinski_harabasz_score as skl_calScore
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# 对类别进行统计,输出一个包含类别和数目信息的字典
def tallyClusters(Clist):
	# 将narray数据转化为list
	S = Clist.tolist()
	# 统计每一类的数量
	classN=dict()
	for i in range(len(S)):
		classN[S[i]] = classN.get(S[i], 0) + 1
	return classN
# 对分类的统计结果进行图像化显示

def paintResult(resultDict):
	# 数值列表
	num_list = []
	# 名字列表
	name_list = []
	# 填充两个列表
	for k,v in resultDict.items():
		name_list.append(k)
		num_list.append(v)
	
	plt.figure()
	plt.title('k-means', color='blue')
	# 画出直方图
	rects = plt.bar(name_list,num_list)
	plt.xticks(name_list)
	# 标注数据
	
	for rect in rects:
		x = rect.get_x()
		width = rect.get_width()
		height = rect.get_height()
		plt.text(x+width/2,height,height,ha='center', va='bottom',fontsize=10)
	
	# 设置打开交互模式而不阻塞
	plt.ion()
	# show出来
	plt.show()
	
	
# k-means聚类，返回分类器和分类结果
def K_Means(data,clusterNum=8,randomState=1,randomTimes=10):
	# 初始化分类器
	kms = slc.KMeans(n_clusters=clusterNum,init='k-means++',n_init=randomTimes)
	# 使用分类器得到每一条记录对应类别的集合
	result = kms.fit_predict(data)
	# 返回得到的结果和分类器
	return result,kms

##
# 绘出肘部图
def elbowFigure(data,min=2,max=10):
	#绘制kmeans肘部图
	#param X 数据集
	#silScore=[]
	#calScore=[]
	# 误差平方和序列
	SSE=[]
	# 从分2类到10类
	for k in range(min,max+1):
		result,kms = K_Means(data,k)
		# 分别获得误差平方和、轮廓系数、卡林斯基-哈拉巴斯指数
		SSE.append(kms.inertia_)
		#silScore.append(skl_silScore(data,result))
		#calScore.append(skl_calScore(data,result))
	# 选择单独显示肘部图
	plt.figure()
	plt.xlabel('K value')
	plt.ylabel('SSE')
	plt.plot(range(min,max+1),SSE,'o-')
	plt.xticks(range(min,max+1))
	plt.ion()
	plt.show()
	
# Main function
def main():
	# 数据导入
	if len(sys.argv) == 1 :
		print("Need a file at least")
	else:
		# 存储属性数据
		data = []
		# 存储公司名称，即键值数据
		names = []
		# 导入数据
		pos = 2 if sys.argv[1]=='-e' else 1
		try:
			
			with open(sys.argv[pos],'r')as f:
				lines = f.readlines()
				propertyName = lines.pop(0)
				for line in lines:
					cells = line.strip().split(',')
					names.append(cells[0])
					data.append([float(cells[i]) for i in range(1,len(cells))])
			'''标准化的地方我去掉了，我查找资料发现标准化实际上会造成数据趋向正态分布'''
			#scaler = StandardScaler()
			#data = scaler.fit_transform(data)
			
			
			
			#print(data)
			if pos == 1 :
				if len(sys.argv)==3 and type(eval(sys.argv[2]))==int:
					pd_data=pd.read_csv(sys.argv[pos])#用于后续输出结果
					result,sorter = K_Means(data,int(sys.argv[2]))
					new_file_name=sys.argv[pos].replace('.','_res_kmeans.')
					print('&&&')
					print(result)
					labels = pd.DataFrame(result,columns=['labels'])
					new_df=pd.concat([pd_data,labels],axis=1)
					new_df.to_csv(new_file_name)
					print("保存到"+new_file_name)
				else:
					result,sorter = K_Means(data)
				finalResult = tallyClusters(result)
				print("[分类及数量]:",finalResult)
				paintResult(finalResult)
				print("[轮廓系数]: "+str(skl_silScore(data,result)))
				print('[Calinski-Harabasz指数]: '+str(skl_calScore(data,result)))
				plt.show()
			else:
				# 绘出肘部图	
				if len(sys.argv)==3:
					elbowFigure(data)
				elif len(sys.argv)==5 and  type(eval(sys.argv[3]))==int and type(eval(sys.argv[4]))==int and int(sys.argv[3]) < int(sys.argv[4]):
					elbowFigure(data, int(sys.argv[3]), int(sys.argv[4]))
			input("[Pressed any key to quit...]")
		except FileNotFoundError:
			print('["'+sys.argv[pos]+'" is not a file!]')
		except IndexError :
			print("[Arguments wrong!]")
# Entrance
main()