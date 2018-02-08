# -*- coding:utf-8 -*-

__author__ = 'gjw'
__date__ = '2018/2/6 9:52'

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
# 已登录的用户可以看到
@login_required
def index():
    # 将g.user传入给模板
    user = g.user
    # 创建用户并展示他们的文章
    posts = [
        {
            'author': {'nickname': 'gjw'},
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
# oid.loginhandle 告诉 Flask-OpenID 这是我们的登录视图函数。
@oid.loginhandler
def login():
    # 我们检查 g.user 是否被设置成一个认证用户，如果是的话将会被重定向到首页。
    # Flask 中的 g 全局变量是一个在请求生命周期中用来存储和共享数据。我敢肯定你猜到了，我们将登录的用户存储在这里(g)。
    if g.user is not None and g.user.is_authenticated:
        # url_for以一种干净的方式为一个给定的视图函数获取URL
        return redirect(url_for('index'))
    form = LoginForm()
    # 验证并且存储表单数据
    if form.validate_on_submit():
        # flask.session 提供了一个更加复杂的服务对于存储和共享数据。
        # 一旦数据存储在会话对象中，在来自同一客户端的现在和任何以后的请求都是可用的。
        # 数据保持在会话中直到会话被明确地删除
        session['remember_me'] = form.remember_me.data
        # oid.try_login 被调用是为了触发用户使用 Flask-OpenID 认证。
        # 该函数有两个参数，用户在 web 表单提供的 openid 以及我们从 OpenID 提供商得到的数据项列表。
        # 因为我们已经在用户模型类中定义了 nickname 和 email，这也是我们将要从 OpenID 提供商索取的。
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
        # OpenID 认证异步发生。如果认证成功的话，Flask-OpenID 将会调用一个注册了 oid.after_login 装饰器的函数。如果失败的话，用户将会回到登陆页面。
        # # flash呈现页面消息
        # flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        # # 这个函数告诉网页浏览器引导到一个不同的页面而不是请求的页面
        # return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    # 验证合法的邮箱地址
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    # 用户为空，创建用户
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    # 登录注册的用户
    login_user(user, remember=remember_me)
    # 如果在 next 页没有提供的情况下，我们会重定向到首页，否则会重定向到 next 页。
    return redirect(request.args.get('next') or url_for('index'))


# 从数据库加载用户
@lm.user_loader
def load_user(id):
    # 请注意在Flask - Login中的用户ids永远是unicode字符串，
    # 因此在我们把id发送给Flask - SQLAlchemy之前，把id转成整型是必须的，否则会报错！
    return User.query.get(int(id))


# 你会记得在登录视图函数中我们检查 g.user 为了决定用户是否已经登录。为了实现这个我们用 Flask 的 before_request 装饰器。
# 任何使用了 before_request 装饰器的函数在接收请求之前都会运行。
@app.before_request
def before_request():
    # 所有请求将会访问到登录用户，即使在模版里
    g.user = current_user


# 登出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



