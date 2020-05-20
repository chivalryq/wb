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
	
	


	

# Birch聚类
def Birch(data,T=0.5,Nclusters=None,branchs=50):
	# 初始化分类器
	bc = slc.Birch(threshold=T, n_clusters=Nclusters, branching_factor=branchs)
	# 使用分类器得到每一条记录对应类别的集合
	result = bc.fit_predict(data)
	# 返回得到的结果和分类器
	return result,bc



## 对于Birch算法的前验分析
def birchCMP(data,TMin,TMax,NcluMin,NcluMax,TStep=0.1,NcluStep=1):
	print("阈值\t聚类个数\t轮廓系数\tCalinski-Harabasz指数\t分类结果")
	bestT_sil=TMin
	bestNclu_sil=NcluMin
	bestT_cal=TMin
	bestNclu_cal=NcluMin
	
	T = []
	Nclu = []
	sil = []
	cal = []
	
	bestSilScore=-1
	bestCalScore=0
	
	fig = plt.figure()
	tDsil = fig.add_subplot(121,projection='3d')
	tDcal = fig.add_subplot(122,projection='3d')
	tDsil.set_title("silhouette Score")
	tDcal.set_title("Calinski-Harabasz Score")
	i = TMin
	while i <= TMax :
		for j in range(NcluMin,NcluMax+1,NcluStep):
			bc = slc.Birch(threshold=i,n_clusters=j)
			result = bc.fit_predict(data)
			finalResult = tallyClusters(result)
			silScore = skl_silScore(data,result)
			calScore = skl_calScore(data,result)
			T.append(i)
			Nclu.append(j)
			sil.append(silScore)
			cal.append(calScore)
			print(i,"\t",j,"\t",silScore,"\t",calScore,"\t", finalResult)
			if silScore > bestSilScore:
				bestSilScore = silScore
				bestT_sil = i
				bestNclu_sil =j
			if calScore > bestCalScore:
				bestCalScore = calScore
				bestT_cal = i
				bestNclu_cal =j
		i = i + TStep
	
	tDsil.bar3d([x-0.2*TStep for x in T], [x-0.2*NcluStep for x in Nclu] ,np.zeros_like(T),dx=0.4*TStep,dy=0.4*NcluStep,dz=sil)
	tDsil.set_xlabel("threshold")
	tDsil.set_ylabel("n_clusters")
	tDsil.set_zlabel("silhouette_score")
	
	tDcal.bar3d([x-0.2*TStep for x in T], [x-0.2*NcluStep for x in Nclu] ,np.zeros_like(T),dx=0.4*TStep,dy=0.4*NcluStep,dz=cal,color="yellow")
	tDcal.set_xlabel("threshold")
	tDcal.set_ylabel("n_clusters")
	tDcal.set_zlabel("Calinski-Harabasz_Score")
	
	print("当阈值（方差）为",bestT_sil,"聚类个数为",bestNclu_sil,"时,轮廓系数最佳")
	print("当阈值（方差）为",bestT_cal,"聚类个数为", bestNclu_cal ,"时,Calinski-Harabasz指数最佳")
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
			#scaler = StandardScaler()
			#data = scaler.fit_transform(data)
			print(data)
			if pos == 1 :
				if len(sys.argv)==4 and type(eval(sys.argv[2]))==float and type(eval(sys.argv[3]))==int:
					result,sorter = Birch(data,float(sys.argv[2]),int(sys.argv[3]))
				elif len(sys.argv)==3 and type(eval(sys.argv[2]))==float:
					result,sorter = Birch(data,float(sys.argv[2]))
				else:
					result,sorter = Birch(data)
				finalResult = tallyClusters(result)
				print("[分类及数量]:",finalResult)
				paintResult(finalResult)
				print("[轮廓系数]:",skl_silScore(data,result))
				print('[Calinski-Harabasz指数]:',skl_calScore(data,result))
				plt.show()
			else:
				if type(eval(sys.argv[3]))==float and type(eval(sys.argv[4]))==float and float(sys.argv[3])<float(sys.argv[4]) and\
				type(eval(sys.argv[5]))==int and type(eval(sys.argv[6]))==int and int(sys.argv[5])<int(sys.argv[6]) :
					# 打印类比结果
					print("in")
					if len(sys.argv)==9 and type(eval(sys.argv[7]))==float and type(eval(sys.argv[8]))==int:
						birchCMP(data,float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), float(sys.argv[7]), int(sys.argv[8]))
					else:
						birchCMP(data,float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
			input("[Pressed any key to quit...]")
		except FileNotFoundError:
			print('["'+sys.argv[pos]+'" is not a file!]')
		except IndexError :
			print("[Arguments wrong!]")

# Entrance
main()