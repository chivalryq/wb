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
	


# OPTICS聚类
def OPTICS(data,simpleInACluster=50,minSize=.05):
	# 初始化分类器
	op = slc.OPTICS(min_samples=simpleInACluster, min_cluster_size=minSize,xi=.05)
	# 使用分类器得到每一条记录对应类别的集合
	result = op.fit_predict(data)
	# 返回得到的结果和分类器
	return result,op

## 对于Birch算法的前验分析
def opticsCMP(data,smplMin,smplMax,sizeMin,sizeMax,smplStep=10,sizeStep=0.1):
	print("样本点数\t最小类尺寸\t轮廓系数\tCalinski-Harabasz指数\t分类结果")
	bestsmpl_sil=smplMin
	bestsize_sil=sizeMin
	bestsmpl_cal=smplMin
	bestsize_cal=sizeMin
	
	smpl = []
	size = []
	sil = []
	cal = []
	
	bestSilScore=-1
	bestCalScore=0
	
	fig = plt.figure()
	tDsil = fig.add_subplot(121,projection='3d')
	tDcal = fig.add_subplot(122,projection='3d')
	tDsil.set_title("silhouette Score")
	tDcal.set_title("Calinski-Harabasz Score")
	j = sizeMin
	for i in range(smplMin,smplMax+1,smplStep):
		while j <= sizeMax :
			op = slc.OPTICS(min_samples=i, min_cluster_size=j)
			result = op.fit_predict(data)
			finalResult = tallyClusters(result)
			silScore = skl_silScore(data,result)
			calScore = skl_calScore(data,result)
			smpl.append(i)
			size.append(j)
			sil.append(silScore)
			cal.append(calScore)
			print(i,"\t",j,"\t",silScore,"\t",calScore,"\t", finalResult)
			if silScore > bestSilScore:
				bestSilScore = silScore
				bestsmpl_sil = i
				bestsize_sil =j
			if calScore > bestCalScore:
				bestCalScore = calScore
				bestsmpl_cal = i
				bestsize_cal =j
			j = j + sizeStep
	
	tDsil.bar3d([x-0.2*smplStep for x in smpl], [x-0.2*sizeStep for x in size] ,np.zeros_like(smpl),dx=0.4*smplStep,dy=0.4*sizeStep,dz=sil)
	tDsil.set_xlabel("min_samples")
	tDsil.set_ylabel("min_cluster_size")
	tDsil.set_zlabel("silhouette_score")
	
	tDcal.bar3d([x-0.2*smplStep for x in smpl], [x-0.2*sizeStep for x in size] ,np.zeros_like(smpl),dx=0.4*smplStep,dy=0.4*sizeStep,dz=cal,color="yellow")
	tDcal.set_xlabel("min_samples")
	tDcal.set_ylabel("min_cluster_size")
	tDcal.set_zlabel("Calinski-Harabasz_Score")
	
	print("当样本点数为",bestsmpl_sil,"最小类尺寸为",bestsize_sil,"时,轮廓系数最佳")
	print("当样本点数为",bestsmpl_cal,"最小类尺寸为", bestsize_cal ,"时,Calinski-Harabasz指数最佳")
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
			#print(data)
			if pos == 1 :
				if len(sys.argv)==4 and type(eval(sys.argv[2]))==int and type(eval(sys.argv[3]))==float:
					result,sorter = OPTICS(data,int(sys.argv[2]),float(sys.argv[3]))
				elif len(sys.argv)==3 and type(eval(sys.argv[2]))==int:
					result,sorter = OPTICS(data,int(sys.argv[2]))
				else:
					result,sorter = OPTICS(data)
				finalResult = tallyClusters(result)
				print("[分类及数量]:",finalResult)
				paintResult(finalResult)
				print("[轮廓系数]:",skl_silScore(data,result))
				print('[Calinski-Harabasz指数]:',skl_calScore(data,result))
				'''保存结果'''
				pd_data=pd.read_csv(sys.argv[pos])#用于后续输出结果
				new_file_name=sys.argv[pos].replace('.','_res_optics.')
				labels = pd.DataFrame(result,columns=['labels'])
				new_df=pd.concat([pd_data,labels],axis=1)
				new_df.to_csv(new_file_name)
				print("保存到"+new_file_name)
				plt.show()

				

			else:
				if type(eval(sys.argv[3]))==int and type(eval(sys.argv[4]))==int and int(sys.argv[3])<int(sys.argv[4]) and\
				type(eval(sys.argv[5]))==float and type(eval(sys.argv[6]))==float and float(sys.argv[5])<float(sys.argv[6]) :
					# 打印类比结果
					print("in")
					if len(sys.argv)==9 and type(eval(sys.argv[7]))==int and type(eval(sys.argv[8]))==float:
						opticsCMP(data,int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7]), float(sys.argv[8]))
					else:
						opticsCMP(data,int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]))
			input("[Pressed any key to quit...]")
		except FileNotFoundError:
			print('["'+sys.argv[pos]+'" is not a file!]')
		except IndexError :
			print("[Arguments wrong!]")

# Entrance
main()