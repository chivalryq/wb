from .utils import read_pickle
import sklearn.cluster as slc
import pandas as pd
def predict_honesty(is_justice_creditaic=0,is_justice_credit=0,is_kcont=0):
   
   #数据预处理,与之前预处理的流程一致
   nega_is_kcont=-is_kcont
   #平均值，标准差是标准化所需的数据，可能会有用归一化的，这里换成最大最小值即可
   avrage=[0.0355,1.46,-0.1922]
   standard_diviation=[0.185,1.860,0.50704]
   data=[is_justice_creditaic,is_justice_credit,nega_is_kcont]

   pre_process_data=[(data[i]-avrage[i])/standard_diviation[i] for i in range(3)]
   #读取保存的模型
   model=read_pickle('./wbserver/data/honesty_sta.pkl')
   
   #新数据集，即刚传入的数据
   X=pd.DataFrame({"is_justice_creditaic":[pre_process_data[0]],
                     "is_justice_credit":[pre_process_data[1]],
                     "nega_is_kcont":[pre_process_data[2]]})
   #print(X)
   result=model.predict(X.values)

   #将结果处理为标签，这里result只有一个值
   tag=get_honesty_tag(result[0])
   return tag

def get_honesty_tag(res):
   if res>=0 and res<=5:
      tags=['企业诚信度较低','企业诚信度较高','企业诚信度极高','企业诚信度低','企业诚信度低','企业诚信度低']
      return tags[res]
   return '企业诚信度预测标签超过预设'

if __name__ == "__main__":
   #这里找一个你知道的原始数据+标签做测试数据
   if predict_honesty(0,20,0)=='企业诚信度低':
      print("test succeeds")
   else:
      print("test fails")