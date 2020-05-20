import pickle
import os

def make_pickle(model,f):
    #model是待序列化的模型
    #f是序列化后保存的文件
    
    file = open(f,'wb') 
    pickle.dump(model,file)
    file.close()

def read_pickle(pkl_name):
    #f是序列化后保存的文件
    #print(os.path.abspath(pkl_name))
    if os.path.getsize(pkl_name) == 0:
        print("file is empty")
    try:
        with open(pkl_name,'rb') as f:
            model=pickle.load(f)
    except FileNotFoundError:
        print(pkl_name+'不存在')
        return None
    return model