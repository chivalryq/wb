import pickle

def make_pickle(model,f):
    #model是待序列化的模型
    #f是序列化后保存的文件
    
    file = open(f,'wb') 
    pickle.dump(model,file)
    file.close()
