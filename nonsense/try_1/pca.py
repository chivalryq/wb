import os
import pandas
pwd=r'C:\Users\jnjga\Desktop\university\服创\ts\Data_FCDS_hashed\'
files=os.listdir(pwd)
df = pd.read_csv(pwd +'\\'+ file_list[0])  
sv_path=r'C:\Users\jnjga\Desktop\university\服创\ts\Data_FCDS_hashed\all.csv'
df.to_csv(sv_path,encoding="utf_8_sig",index=False)
ipat=r'C:\Users\jnjga\Desktop\university\服创\ts\Data_FCDS_hashed\intangible_patent.csv'
df = pandas.read_csv(file)# 返回一个DataFrame对象
#n_rows = df.head(10) #获取前n行数据，返回的依旧是个DataFrame
#column_names = df.columns   #获取所有的列名
#dimensions = df.shape #获取数据的shape
#print(df,n_rows,column_names,dimensions)

print(df.shape)