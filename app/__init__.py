# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/2/6 9:50'
"""
    初始化脚本
"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 导入配置文件
app.config.from_object('config')
# 初始化数据库
db = SQLAlchemy(app)

from app import views, models