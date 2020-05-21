import platform
SQLALCHEMY_DATABASE_URI = 'mysql://root:@Qzp000209@localhost/wbdb' #数据库设置
SQLALCHEMY_TRACK_MODIFICATIONS= True
ROOT_PATH='/root' if platform.system()=='Linux' else '.'
#服务器项目所在根目录和用vscode打开的默认目录