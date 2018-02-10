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


# 编辑用户信息表单
class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if not user:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True
