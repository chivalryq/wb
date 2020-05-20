#对企业竞争风险的预处理
#priclasecam字段的单位明显不统一

import pandas as pd
import numpy as np
if __name__ == "__main__":
    risk=pd.read_csv("./risk/data/risk_p_add.csv")
    # print(risk)
    
    max_min_scaler = lambda x : (x-np.min(x))/(np.max(x)-np.min(x))
    
    colname=['is_bp','is_bra','pledgenum','taxunpaidnum','priclasecam']
    for col in colname:
        #归一化
        risk[col]=risk[[col]].apply(max_min_scaler)
    risk.to_csv('risk/data/risk_a_n.csv')
    print("Save to risk/data/risk_a_n.csv")