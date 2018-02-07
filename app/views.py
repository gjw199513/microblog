# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/2/6 9:52'

from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    # 展示用户昵称
    user = {'nickname': 'gjw'}
    # 创建用户并展示他们的文章
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


# methods 参数:参数告诉 Flask 这个视图函数接受 GET 和 POST 请求。如果不带参数的话，视图只接受 GET 请求。
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 验证并且存储表单数据
    if form.validate_on_submit():
        # flash呈现页面消息
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        # 这个函数告诉网页浏览器引导到一个不同的页面而不是请求的页面
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])