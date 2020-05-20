import sys
import pandas as pd
import numpy as np
import sklearn.datasets as sld 
import sklearn.cluster as slc
from sklearn.metrics import silhouette_score as skl_silScore
from sklearn.metrics import calinski_harabasz_score as skl_calScore
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
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
	
	

# affinity聚类
def Affinity(data,pre=-50,dam=0.5):
	# 初始化分类器
	af = slc.AffinityPropagation(preference=pre,damping=dam)
	# 使用分类器得到每一条记录对应类别的集合
	result = af.fit_predict(data)
	# 返回得到的结果和分类器
	return result,af

## 对于DBSCAN算法的前验分析
def affinityCMP(data,preMin,preMax,damMin,damMax,preStep=1,damStep=0.1):
	print("偏好\t阻尼系数\t轮廓系数\tCalinski-Harabasz指数\t分类结果")
	bestpre_sil=preMin
	bestdam_sil=damMin
	bestpre_cal=preMin
	bestdam_cal=damMin
	
	pre = []
	dam = []
	sil = []
	cal = []
	
	bestSilScore=-1
	bestCalScore=0
	
	fig = plt.figure()
	tDsil = fig.add_subplot(121,projection='3d')
	tDcal = fig.add_subplot(122,projection='3d')
	tDsil.set_title("silhouette Score")
	tDcal.set_title("Calinski-Harabasz Score")
	j = damMin
	for i in range(preMin,preMax+1,preStep):
		while j <= amMax :
			af = slc.AffinityPropagation(preference=i,damping=j)
			result = af.fit_predict(data)
			finalResult = tallyClusters(result)
			silScore = skl_silScore(data,result)
			calScore = skl_calScore(data,result)
			pre.append(i)
			dam.append(j)
			sil.append(silScore)
			cal.append(calScore)
			print(i,"\t",j,"\t",silScore,"\t",calScore,"\t", finalResult)
			if silScore > bestSilScore:
				bestSilScore = silScore
				bestpre_sil = i
				bestdam_sil =j
			if calScore > bestCalScore:
				bestCalScore = calScore
				bestpre_cal = i
				bestdam_cal =j
			j = j + damStep
	
	tDsil.bar3d([x-0.2*preStep for x in pre], [x-0.2*damStep for x in dam] ,np.zeros_like(pre),dx=0.4*preStep,dy=0.4*damStep,dz=sil)
	tDsil.set_xlabel("pre")
	tDsil.set_ylabel("min_samples")
	tDsil.set_zlabel("silhouette_score")
	
	tDcal.bar3d([x-0.2*preStep for x in pre], [x-0.2*damStep for x in dam] ,np.zeros_like(pre),dx=0.4*preStep,dy=0.4*damStep,dz=cal,color="yellow")
	tDcal.set_xlabel("pre")
	tDcal.set_ylabel("min_samples")
	tDcal.set_zlabel("Calinski-Harabasz_Score")
	
	print("当偏好为",bestpre_sil,"阻尼系数为",bestdam_sil,"时,轮廓系数最佳")
	print("当偏好为",bestpre_cal,"阻尼系数为", bestdam_cal ,"时,Calinski-Harabasz指数最佳")
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
		pos = 2 if sys.argv[1]=='-c' else 1
		try:	
			with open(sys.argv[pos],'r')as f:
				lines = f.readlines()
				propertyName = lines.pop(0)
				for line in lines:
					cells = line.strip().split(',')
					names.append(cells[0])
					data.append([float(cells[i]) for i in range(1,len(cells))])
			scaler = StandardScaler()
			data = scaler.fit_transform(data)
			print(data)
			if pos == 1 :
				if len(sys.argv)==4 and type(eval(sys.argv[2]))==int and type(eval(sys.argv[3]))==int:
					result,sorter = Affinity(data,int(sys.argv[2]),int(sys.argv[3]))
				else:
					result,sorter = Affinity(data)
				finalResult = tallyClusters(result)
				print("[分类及数量]:",finalResult)
				paintResult(finalResult)
				print("[轮廓系数]:",skl_silScore(data,result))
				print('[Calinski-Harabasz指数]:',skl_calScore(data,result))
				plt.show()
			else:
				if type(eval(sys.argv[3]))==int and type(eval(sys.argv[4]))==int and int(sys.argv[3])<int(sys.argv[4]) and\
				type(eval(sys.argv[5]))==float and type(eval(sys.argv[6]))==float and float(sys.argv[5])<float(sys.argv[6]) :
					# 打印类比结果	
					print("in")
					if len(sys.argv)==9 and type(eval(sys.argv[7]))==int and type(eval(sys.argv[8]))==float:
						affinityCMP(data,int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7]), float(sys.argv[8]))
					else:
						affinityCMP(data,int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))
			input("[Pressed any key to quit...]")
		except FileNotFoundError:
			print('["'+sys.argv[pos]+'" is not a file!]')
		except IndexError :
			print("[Arguments wrong!]")

# Entrance
main()