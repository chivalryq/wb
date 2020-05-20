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

from .utils import check

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


# dbscan聚类，
def Dbscan(data,maxDis=5,simpleInACluster=10):
	# 初始化分类器
	db = slc.DBSCAN(eps=maxDis,min_samples=simpleInACluster,metric='euclidean')
	# 使用分类器得到每一条记录对应类别的集合
	result = db.fit_predict(data)
	# 返回得到的结果和分类器
	return result,db



## 对于DBSCAN算法的前验分析
def dbscanCMP(data,epsMin,epsMax,smplMin,smplMax,epsStep=1,smplStep=1):
	print("半径\t簇内个数\t轮廓系数\tCalinski-Harabasz指数\t分类结果")
	bestEps_sil=epsMin
	bestSmpl_sil=smplMin
	bestEps_cal=epsMin
	bestSmpl_cal=smplMin
	
	eps = []
	smpl = []
	sil = []
	cal = []
	
	bestSilScore=-1
	bestCalScore=0
	
	fig = plt.figure()
	tDsil = fig.add_subplot(121,projection='3d')
	tDcal = fig.add_subplot(122,projection='3d')
	tDsil.set_title("silhouette Score")
	tDcal.set_title("Calinski-Harabasz Score")
	#改成了兼容float
	for i in np.arange(epsMin,epsMax,epsStep):
		for j in np.arange(smplMin,smplMax+1,smplStep):
			db = slc.DBSCAN(eps=i,min_samples=j,metric='euclidean')
			result = db.fit_predict(data)
			finalResult = tallyClusters(result)
			silScore = skl_silScore(data,result)
			calScore = skl_calScore(data,result)
			eps.append(i)
			smpl.append(j)
			sil.append(silScore)
			cal.append(calScore)
			print(i,"\t",j,"\t",silScore,"\t",calScore,"\t", finalResult)
			if silScore > bestSilScore:
				bestSilScore = silScore
				bestEps_sil = i
				bestSmpl_sil =j
			if calScore > bestCalScore:
				bestCalScore = calScore
				bestEps_cal = i
				bestSmpl_cal =j
	
	tDsil.bar3d([x-0.2*epsStep for x in eps], [x-0.2*smplStep for x in smpl] ,np.zeros_like(eps),dx=0.4*epsStep,dy=0.4*smplStep,dz=sil)
	tDsil.set_xlabel("eps")
	tDsil.set_ylabel("min_samples")
	tDsil.set_zlabel("silhouette_score")
	
	tDcal.bar3d([x-0.2*epsStep for x in eps], [x-0.2*smplStep for x in smpl] ,np.zeros_like(eps),dx=0.4*epsStep,dy=0.4*smplStep,dz=cal,color="yellow")
	tDcal.set_xlabel("eps")
	tDcal.set_ylabel("min_samples")
	tDcal.set_zlabel("Calinski-Harabasz_Score")
	
	print("当半径为",bestEps_sil,"簇内个数为",bestSmpl_sil,"时,轮廓系数最佳")
	print("当半径为",bestEps_cal,"簇内个数为", bestSmpl_cal ,"时,Calinski-Harabasz指数最佳")
	plt.ion()
	plt.show()
	

# Main function
def main():
	# 数据导入

	print([check(x) for x in sys.argv])
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
			#print(data)
			if pos == 1 :
				if len(sys.argv)==4 and check(sys.argv[2]) in (float,int) and check(sys.argv[3])==int:
					
					result,sorter = Dbscan(data,float(sys.argv[2]),int(sys.argv[3]))
					pd_data=pd.read_csv(sys.argv[pos])#用于后续输出结果
					new_file_name=sys.argv[pos].replace('.','_res_dbscan.')
					#print(result)
					labels = pd.DataFrame(result,columns=['labels'])
					new_df=pd.concat([pd_data,labels],axis=1)
					new_df.to_csv(new_file_name)
					print("保存到"+new_file_name)
				else:
					result,sorter = Dbscan(data)
				finalResult = tallyClusters(result)
				print("[分类及数量]:",finalResult)
				paintResult(finalResult)
				print("[轮廓系数]:",skl_silScore(data,result))
				print('[Calinski-Harabasz指数]:',skl_calScore(data,result))
				plt.show()
			else:
				if check(sys.argv[3]) in (float,int) and check(sys.argv[4]) in (float,int) and float(sys.argv[3])<float(sys.argv[4]) and\
				check(sys.argv[5]) in (float,int) and check(sys.argv[6]) in (float,int) and float(sys.argv[5])<float(sys.argv[6]) :
					print("test")
					# 打印类比结果	
					if len(sys.argv)==9 and check(sys.argv[7]) in (float,int) and check(sys.argv[8]) in (float,int):
						dbscanCMP(data,float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7]), float(sys.argv[8]))
					else:
						dbscanCMP(data,float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))
			input("[Pressed any key to quit...]")
		except FileNotFoundError:
			print('["'+sys.argv[pos]+'" is not a file!]')
		except IndexError :
			print("[Arguments wrong!]")
# Entrance
main()