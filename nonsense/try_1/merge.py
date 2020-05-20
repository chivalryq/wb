import os
import pandas as pd
pwd=r'C:\Users\jnjga\Desktop\university\服创\ts\Data_FCDS_hashed'
sv_path=os.path.join(pwd,'all.csv')
if os.path.exists(sv_path):
    os.remove(sv_path)
files=os.listdir(pwd)
files=files[:8]
df = pd.read_csv(pwd +'\\'+ files[0])  
df.to_csv(sv_path,encoding="utf_8_sig",index=False)
all_df=pd.read_csv(sv_path)

#循环遍历列表中各个CSV文件名，并追加到合并后的文件
for i in range(1,len(files)):
    print(files[i])
    new_df = pd.read_csv(pwd + '\\'+ files[i], encoding='ISO-8859-1')
    all_df = pd.merge(all_df,new_df,how = 'outer',on='entname')

os.remove(sv_path)
all_df.to_csv(sv_path,encoding="utf_8_sig",index=False)
