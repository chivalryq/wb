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
#用以制作持久化的模型 
from .mk_pickle import make_pickle

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
	
	


# mean-shift聚类
def Mean_Shift(data,qtl=0.2,nPoint=50):
	bandwidth = slc.estimate_bandwidth(data, quantile=qtl, n_samples=nPoint)
	ms = slc.MeanShift(bandwidth=bandwidth, bin_seeding=True)
	result = ms.fit_predict(data)
	# 返回得到的结果和分类器
	return result,ms

def Mean_Shift_bandwidth(data,bandwidth):
	ms = slc.MeanShift(bandwidth=bandwidth)
	result = ms.fit(data).labels_
	# 返回得到的结果和分类器
	return result,ms


## 对于mean-shift算法的前验分析
def meanShiftCMP(data,bd_min,bd_max,bdStep=0.1):
	print("bandwidth\t轮廓系数\tCalinski-Harabasz指数\t分类结果")

	bestbd_sil=bd_min
	bestbd_cal=bd_min
	
	bd=[]
	sil = []
	cal = []
	
	bestSilScore=0
	bestCalScore=0
	
	fig = plt.figure()
	tDsil = fig.add_subplot(121)
	tDcal = fig.add_subplot(122)
	tDsil.set_title("silhouette Score")
	tDcal.set_title("Calinski-Harabasz Score")

	for i in np.arange(bd_min,bd_max,bdStep):
		bandwidth=i
		ms = slc.MeanShift(bandwidth=bandwidth, bin_seeding=True)
		result = ms.fit_predict(data)
		finalResult = tallyClusters(result)
		silScore = skl_silScore(data,result)
		calScore = skl_calScore(data,result)
		bd.append(i)
		
		sil.append(silScore)
		cal.append(calScore)
		print(i,"\t",silScore,"\t",calScore,"\t", finalResult)
		if silScore > bestSilScore:
			bestSilScore = silScore
			bestbd_sil = i
			
		if calScore > bestCalScore:
			bestCalScore = calScore
			bestbd_cal = i
			
		
	tDsil.plot([x for x in np.arange(bd_min,bd_max,bdStep)],[y for y in sil])
	tDsil.set_xlabel("bandwidth")
	tDsil.set_ylabel("silhouette_score")
	tDcal.plot([x for x in np.arange(bd_min,bd_max,bdStep)],[y for y in cal])
	tDcal.set_xlabel("bandwidth")
	tDcal.set_ylabel("Calinski-Harabasz_Score")
	# tDsil.bar3d([x-0.2*qtlStep for x in qtl], [x-0.2*nPointStep for x in nPoint] ,np.zeros_like(qtl),dx=0.4*qtlStep,dy=0.4*nPointStep,dz=sil)
	# tDsil.set_xlabel("quantile")
	# tDsil.set_ylabel("n_samples")
	# tDsil.set_zlabel("silhouette_score")
	
	# tDcal.bar3d([x-0.2*qtlStep for x in qtl], [x-0.2*nPointStep for x in nPoint] ,np.zeros_like(qtl),dx=0.4*qtlStep,dy=0.4*nPointStep,dz=cal,color="yellow")
	# tDcal.set_xlabel("quantile")
	# tDcal.set_ylabel("n_samples")
	# tDcal.set_zlabel("Calinski-Harabasz_Score")
	
	print("当bandwidth为",bestbd_sil,"时,轮廓系数最佳")
	print("当bandwidth为",bestbd_cal,"时,Calinski-Harabasz指数最佳")
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
				#cnt=0
				for line in lines:
					#print(cnt)
					#cnt=cnt+1
					cells = line.strip().split(',')
					names.append(cells[0])
					data.append([float(cells[i]) for i in range(1,len(cells))])
			#scaler = StandardScaler()
			#data = scaler.fit_transform(data)
			#print(data)
			if pos == 1 :
				if len(sys.argv)==4 and type(eval(sys.argv[2]))in (int,float) and type(eval(sys.argv[3]))==int:
					result,sorter = Mean_Shift(data,float(sys.argv[2]),int(sys.argv[3]))
				elif len(sys.argv)==3 and type(eval(sys.argv[2]) in (int,float)):
					result,sorter=Mean_Shift_bandwidth(data,float(sys.argv[2]))
				else:
					result,sorter = Mean_Shift(data)

				#持久化该模型
				pkl_filename=sys.argv[pos].split('.')[0]+'.pkl'
				make_pickle(sorter,pkl_filename)
				print("模型已保存至"+pkl_filename)

				
				finalResult = tallyClusters(result)
				print("[分类及数量]:",finalResult)
				paintResult(finalResult)
				print("[轮廓系数]:",skl_silScore(data,result))
				print('[Calinski-Harabasz指数]:',skl_calScore(data,result))

				'''保存结果'''
				pd_data=pd.read_csv(sys.argv[pos])#用于后续输出结果
				new_file_name=sys.argv[pos].replace('.','_res_meanshift.')
				labels = pd.DataFrame(result,columns=['labels'])
				new_df=pd.concat([pd_data,labels],axis=1)
				new_df.to_csv(new_file_name)
				

				plt.show()
			else:
				if type(eval(sys.argv[3]))in (int,float) and type(eval(sys.argv[4]))in (int,float) and float(sys.argv[3])<float(sys.argv[4]) :
					# 打印类比结果	
					if len(sys.argv)==6 and type(eval(sys.argv[5]))in (int,float):
						meanShiftCMP(data,float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
					else:
						meanShiftCMP(data,float(sys.argv[3]), float(sys.argv[4]))
			input("[Pressed any key to quit...]")
		except FileNotFoundError:
			print('["'+sys.argv[pos]+'" is not a file!]')
		except IndexError :
			print("[Arguments wrong!]")
# Entrance
main()