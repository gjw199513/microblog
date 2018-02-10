# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/2/6 10:54'

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from app.models import User


# 登录表单
class LoginForm(Form):
    # DataRequired：对应的域是或否为空
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


