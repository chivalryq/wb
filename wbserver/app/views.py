from . import app
from flask import request,jsonify,render_template

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
    return jsonify(tags=tags)