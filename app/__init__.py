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
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

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


# 异常时发送邮件
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


# 文件日志
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    # 名称为 microblog.log。
    # 我们使用了 RotatingFileHandler 以至于生成的日志的大小是有限制的。
    # 在这个例子中，我们的日志文件的大小限制在 1 兆，我们将保留最后 10 个日志文件作为备份。
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    # logging.Formatter 类能够定制化日志信息的格式。
    # 我们写一个时间戳，日志记录级别和消息起源于以及日志消息和堆栈跟踪的文件和行号
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')