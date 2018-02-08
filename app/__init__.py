# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/2/6 9:50'
"""
    初始化脚本
"""
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
app = Flask(__name__)
# 导入配置文件
app.config.from_object('config')
# 初始化数据库
db = SQLAlchemy(app)

# 配置登录
lm = LoginManager()
lm.init_app(app)
# 登录的视图
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
from app import views, models