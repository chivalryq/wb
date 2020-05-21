from . import app
from flask import request,jsonify,render_template,request
from .predict import *
@app.route('/')
def index():
    return str(app.url_map)

from .models import *
@app.route('/tags',methods=['POST'])
def tags():
    entnames=request.form['entnames']
    if entnames is None:
        print('None')
    entnames=entnames.split(',')

    # com_tags=[]
    # inno_tags=[]
    # net_tags=[]
    all_tags=[]
    for entname in entnames:
        all_tags.append(get_tags(entname))
    tags={}
    for i in range(len(entnames)):
        tags[entnames[i]]=all_tags[i]
    return str(tags).replace("'",'"')
    # return jsonify(tags=tags)
@app.route('/query')
def query():
    page=''
    with open('templates/index.html') as f:
        return page.join(f.readlines())

@app.route('/predict')
def predict():

    tags=[]
    
    data=request.values['data']
    
    is_justice_creditaic=data.get('is_justice_creditaic',0)
    is_justice_credit=data.get('is_justice_credit',0)
    is_kcont=data.get('is_kcont',0)
    tags.append(predict_honesty(is_justice_creditaic,is_justice_credit,is_kcont))

    regcap=data.get('regcap',0)
    investnum=data.get('investnum',0)
    branchnum=data.get('branchnum',0)
    empnum=data.get('empnum',0)
    tags.append(predict_scale(regcap,investnum,branchnum,empnum))
    
    is_bra=data.get('is_bra',0)
    pledgenum=data.get('pledgenum',0)
    taxunpaidnum=data.get('taxunpaidnum',0)
    priclasecam=data.get('priclasecam',0)
    is_brap=data.get('is_brap',0)
    is_punish=data.get('is_punish',0)
    tags.append(predict_risk(is_bra,pledgenum,taxunpaidnum,priclasecam,is_brap,is_punish))
    
    passpercent=data.get('passpercent',0)
    bidnum=data.get('bidnum',0)
    is_infob=data.get('is_infob',0)
    is_infoa=data.get('is_infoa',0)
    tags.append(predict_competition(passpercent,bidnum,is_infob,is_infoa))
    
    return jsonify(tags=tags)