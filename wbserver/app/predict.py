from .utils import read_pickle
import sklearn.cluster as slc
import pandas as pd
from .settings import ROOT_PATH
from os.path import join
def predict_scale(regcap=0, investnum=0, branchnum=0, empnum=0):
    # 数据预处理,与之前预处理的流程一致
    # 归一化
    Max = [12000000, 13, 22, 216]
    Min = [0, 0, 0, 0]
    data = [regcap, investnum, branchnum, empnum]
    pre_process_data = [(data[i] - Min[i]) / (Max[i] - Min[i]) for i in range(4)]
    # 读取保存的模型
    model = read_pickle(join(ROOT_PATH,'wbserver/data/scale.pkl'))

    # 新数据集，即刚传入的数据
    X = pd.DataFrame({"regcap": [pre_process_data[0]],
                      "investnum": [pre_process_data[1]],
                      "branchnum": [pre_process_data[2]],
                      "empnum": [pre_process_data[3]]})
    # print(X)
    result = model.predict(X.values)

    # 将结果处理为标签，这里result只有一个值
    tag = get_scale_tag(result[0])
    return tag



def predict_honesty(is_justice_creditaic=0,is_justice_credit=0,is_kcont=0):
   
   if is_justice_creditaic<=0 and is_justice_credit<=0 and is_kcont<=0:
       tag='企业诚信度一般'
   #数据预处理,与之前预处理的流程一致
   nega_is_kcont=-is_kcont
   #平均值，标准差是标准化所需的数据，可能会有用归一化的，这里换成最大最小值即可
   avrage=[0.0355,1.46,-0.1922]
   standard_diviation=[0.185,1.860,0.50704]
   data=[is_justice_creditaic,is_justice_credit,nega_is_kcont]

   pre_process_data=[(data[i]-avrage[i])/standard_diviation[i] for i in range(3)]
   #读取保存的模型
   model=read_pickle(join(ROOT_PATH,'wbserver/data/honesty_sta.pkl'))
   
   #新数据集，即刚传入的数据
   X=pd.DataFrame({"is_justice_creditaic":[pre_process_data[0]],
                     "is_justice_credit":[pre_process_data[1]],
                     "nega_is_kcont":[pre_process_data[2]]})
   #print(X)
   result=model.predict(X.values)

   #将结果处理为标签，这里result只有一个值
   tag=get_honesty_tag(result[0])
   return tag



def predict_risk(is_bra=0,pledgenum=0,taxunpaidnum=0,priclasecam=0,is_brap=0,is_punish=0):
    
    # 数据预处理,与之前预处理的流程一致
    # 归一化
    is_bp=is_brap+is_punish
    if(priclasecam>=100000):
        pre_priclasecam=pledgenum/10000
    else:
        pre_priclasecam=pledgenum
    Max = [4,6,13259765.86,25000,13]
    Min = [0, 0, 0, 0, 0]
    data = [is_bra,pledgenum,taxunpaidnum,pre_priclasecam,is_bp]
    pre_process_data = [(data[i] - Min[i]) / (Max[i] - Min[i]) for i in range(5)]
    tag=get_risk_tag(pre_process_data)
    return tag


def predict_competition(passpercent=0, bidnum=0, is_infob=0, is_infoa=0):
    # 独热编码
    if is_infoa == 0:
        is_infoa_1 = 1
        is_infoa_2 = 0
    if is_infoa == 1:
        is_infoa_1 = 0
        is_infoa_2 = 1
    tags = ['竞争力一般', '竞争力弱', '竞争力强']
    if (passpercent >= 0.75) and (passpercent <= 1) and (bidnum >= 0) and (bidnum <= 1) and (is_infob >= 1) and (is_infob <= 2) and (is_infoa_1 >= 0) and (is_infoa_1 <= 1) and (is_infoa_2 >= 0) and (is_infoa_2 <= 1):
        return tags[2]
    elif (passpercent >= 0) and (passpercent <= 0.5) and (bidnum == 0) and (is_infob == 0) and (is_infoa_1 == 1) and (is_infoa_2 == 0):
        return tags[1]
    elif (passpercent >= 0.6) and (passpercent <= 1) and (bidnum >= 0) and (bidnum <= 123) and (is_infob == 0) and (is_infoa_1 >= 0) and (is_infoa_1 <= 1) and (is_infoa_2 >= 0) and (is_infoa_2 <= 1):
        return tags[0]
    return '企业竞争力预测标签超过预设'

def get_honesty_tag(res):
   if res>=0 and res<=5:
      tags=['企业诚信度较低','企业诚信度较高','企业诚信度极高','企业诚信度低','企业诚信度低','企业诚信度低']
      return tags[res]
   return '企业诚信度预测标签超过预设'
      

def get_risk_tag(data):
    is_bra,pledgenum,taxunpaidnum,priclasecam,is_bp=data
    #由于需要数据辅助获得标签，这里需要传入data参数
    tags=['低经营风险','中等经营风险','高经营风险']
    level=0

    #在边界内的数据    
    if is_bra>=0.75 \
       or priclasecam>0.45 \
       or is_bp >= 0.75 \
       or taxunpaidnum >=0.75 \
       or pledgenum >=0.9:
        level=2
    elif is_bra>=0.25 or pledgenum>=0.6 or priclasecam+is_bp>=0.16:
        level=1
    else:
        level=0
    #任何超出边界的数据
    for x in data:
        if x>=1:
            level=2
    
    return tags[level]

def get_scale_tag(res):
    if res >= 0 and res <= 2:
        tags = ['企业规模中等', '企业规模小', '企业规模大']
        return tags[res]
    return '企业规模预测标签超过预设'



if __name__ == "__main__":
   #这里找一个你知道的原始数据+标签做测试数据
   if predict_honesty(0,20,0)=='企业诚信度低' \
      and  predict_competition(0.940380313, 1, 0, 0) == '竞争力一般' \
      and predict_scale(5010000, 0, 0, 8) == '企业规模大' \
      and predict_risk(0,5,0,0,0,0) == '中等经营风险':
      print("test succeeds")
   else:
      print("test fails")