from . import db

class Competition(db.Model):
    entname=db.Column(db.String(40),primary_key=True)
    passpercent=db.Column(db.Float)
    bidnum=db.Column(db.Integer)
    is_infob=db.Column(db.Integer)
    is_infoa_1=db.Column(db.Integer)
    is_infoa_2=db.Column(db.Integer)
    tag=db.Column(db.String(10))

class Scale(db.Model):
    entname=db.Column(db.String(40),primary_key=True)
    regcap=db.Column(db.Integer)
    investnum=db.Column(db.Integer)
    branchnum=db.Column(db.Integer)
    empnum=db.Column(db.Integer)
    tag=db.Column(db.String(10))

class Innovation(db.Model):
    entname=db.Column(db.String(40),primary_key=True)
    icopy_num=db.Column(db.Integer)
    ipat_num=db.Column(db.Integer)
    ibrand_num=db.Column(db.Integer)
    idom_num=db.Column(db.Integer)
    tag=db.Column(db.String(10))

class Network(db.Model):
    entname = db.Column(db.String(40),primary_key=True)
    idom_num = db.Column(db.Integer)
    sum = db.Column(db.Integer)
    shopnum = db.Column(db.Integer)
    tag=db.Column(db.String(10))

class Risk(db.Model):
    entname = db.Column(db.String(40), primary_key=True)
    is_bra = db.Column(db.Float)
    pledgenum = db.Column(db.Float)
    taxunpaidnum = db.Column(db.Float)
    priclasecam = db.Column(db.Float)
    is_bp=db.Column(db.Float)
    labels=db.Column(db.Float)
    tag=db.Column(db.String(10))

class Honesty(db.Model):
    entname = db.Column(db.String(40), primary_key=True)
    is_justice_creditaic=db.Column(db.Integer)
    is_justice_credit=db.Column(db.Integer)
    nega_is_kcont=db.Column(db.Integer)
    labels=db.Column(db.Integer)
    tag = db.Column(db.String(10))

def get_tags(entname):
    return [get_com_tag(entname),get_hon_tag(entname),get_inno_tag(entname),get_net_tag(entname),get_risk_tag(entname),get_sca_tag(entname)]

def get_sca_tag(entname):
    com = Scale.query.filter_by(entname=entname).first()
    if com is None:
        return '无企业规模数据'
    return com.tag

def get_hon_tag(entname):
    com = Honesty.query.filter_by(entname=entname).first()
    if com is None:
        return '诚信一般'
    return com.tag

def get_risk_tag(entname):
    com = Honesty.query.filter_by(entname=entname).first()
    if com is None:
        return '无经营风险'
    return com.tag

def get_com_tag(entname):
    com=Competition.query.filter_by(entname=entname).first()
    if com is None:
        return '无竞争力数据'
    return com.tag

def get_inno_tag(entname):
    inno = Innovation.query.filter_by(entname=entname).first()
    if inno is None:
        return '企创新力一般'
    return inno.tag

def get_net_tag(entname):
    net = Network.query.filter_by(entname=entname).first()
    if net is None:
        return '网络影响力一般'
    return net.tag