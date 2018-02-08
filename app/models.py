# -*- coding:utf-8 -*-


__author__ = 'gjw'
__date__ = '2018/2/7 9:44'

from app import db
from hashlib import md5

# 用户类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # 它是被构建成一个 db.relationship 字段。
    # 对于一个一对多的关系，db.relationship 字段通常是定义在“一”这一边。
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Flask-Login 扩展需要在我们的 User 类中实现一些特定的方法。
    # 但是类如何去实现这些方法却没有什么要求。

    # 这个方法应该只返回 True，除非表示用户的对象因为某些原因不允许被认证
    @property
    def is_authenticated(self):
        return True

    # is_active方法应该返回True，除非是用户是无效的，比如因为他们的账号是被禁止。
    @property
    def is_active(self):
        return True

    # is_anonymous 方法应该返回 True，如果是匿名的用户不允许登录系统。
    @property
    def is_anonymous(self):
        return False
    # is_authenticated=True
    # is_active = True
    # is_anonymous = False

    # get_id 方法应该返回一个用户唯一的标识符，以 unicode 格式
    def get_id(self):
        return str(self.id)

    # User 的方法 avatar 返回用户图片的 URL，以像素为单位缩放成要求的尺寸。
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

    # 打印这个类的方式
    def __repr__(self):
        return '<User %r>' % (self.nickname)


# 用户编写的blog
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    # 初始化外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
