from hopkins import hopkins

import os
import pandas as pd
import numpy as np

def exception():
    file=r'C:\Users\jnjga\Desktop\university\服创\data\经营异常\经营异常.csv'
    #经营异常z标准化
    #new_df = pd.read_csv(file, encoding='ISO-8859-1',usecols=['Zis_bra','Zis_brap','Ztaxunpaidnum'])
    #经营异常中单个数据检查
    new_df = pd.read_csv(file, encoding='ISO-8859-1',usecols=['Ztaxunpaidnum'])
    return new_df
def rnd():
    new_df=pd.DataFrame(np.random.random((100,3)))
    return new_df
#商标与信誉
def mark():
    file=r'C:\Users\jnjga\Desktop\university\服创\data\商标与信誉\商标与信誉_6变量_无主键.csv'
    #new_df = pd.read_csv(file, encoding='ISO-8859-1',usecols=['is_infoa','is_infob','level_rank','is_jnsn','is_kcont','is_justice_creditaic'])
    #商标与信誉中单个数据检查
    new_df = pd.read_csv(file, encoding='ISO-8859-1',usecols=['is_justice_creditaic'])
    return new_df

def knowledge():
    file=r'C:\Users\jnjga\Desktop\university\服创\data\知识产权\知识产权.csv'
    #new_df = pd.read_csv(file, encoding='ISO-8859-1',usecols=['ibrand_num','ipat_num','icopy_num','idom_num'])
    #商标与信誉中单个数据检查
    new_df = pd.read_csv(file, encoding='ISO-8859-1',usecols=['idom_num'])
    #print(new_df)
    return new_df

def other():
    file=r'C:\Users\jnjga\Desktop\university\服创\data\Data_FCDS_hashed\administrative_punishment.csv'
    new_df=pd.read_csv(file,usecols=['is_punish'])
    return new_df

def others():
    d=r'C:\Users\jnjga\Desktop\university\服创\data\Data_FCDS_hashed'
    files=os.listdir(d)
    dfs=[]
    for file in files:
        try:
            df=pd.read_csv(os.path.join(d,file), encoding='ISO-8859-1')
            del df['entname']
            hs=hopkins(df)
        except:
            continue
        dfs.append(df)
        print(file+' Hopkins=',end='')
        print(hopkins(df))
        
    return dfs

if __name__ == "__main__":
    # df=other()
    # hop=hopkins(df)
    # print(hop)
    dfs=others()
    #for df in dfs:
        #print(hopkins(df))