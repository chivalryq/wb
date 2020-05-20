import pandas as pd
import sys
import os

def main():
	if len(sys.argv) == 1 :
		print("Need a file at least")
	else:
		try:
			# 导入数据
			csvData = pd.read_csv(sys.argv[1],index_col=0)
			print("[Before encoding]")	
			print(csvData)
			# 确定进行独热处理的数据属性名
			if len(sys.argv)==2 :
				properties=list(input("请输入要进行独热编码的属性名称，以空格隔开：").strip().split(' '))
			else:
				properties = sys.argv[2:]
			print(properties)
			# 处理数据
			for pro in [column for column in csvData]:
				if pro in properties:
					dummies = pd.get_dummies(csvData[pro],prefix=pro)
					csvData.drop(columns=pro,inplace=True)
					csvData = csvData.join(dummies)
			print("[After encoding]")	
			print(csvData)
			# 导出数据到新文件
			csvData.to_csv(os.path.splitext(sys.argv[1])[0]+"_new.csv")

			print("[newFile's name is ]:"+ os.path.splitext(sys.argv[1])[0]+"_new.csv" )
		except FileNotFoundError:
			print('["'+sys.argv[1]+'" is not a file!]')
		except IndexError :
			print("[Attribute name wrong!]")
main()