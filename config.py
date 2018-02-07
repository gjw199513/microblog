# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/2/6 10:47'

import os
# 激活跨站点请求伪造
CSRF_ENABLED = True
# 上面的参数必须激活
# 建立一个加密的令牌，用于验证表单
SECRET_KEY = 'you-will-never-guess'

# openid提供者
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]



basedir = os.path.abspath(os.path.dirname(__file__))
# mysql数据配置
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:gjw605134015@localhost:3306/microblog"
# SQLALCHEMY_TRACK_MODIFICATIONS = True

# sqlite数据库配置
# 数据库文件路径
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
#  SQLAlchemy-migrate 数据文件存储
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True