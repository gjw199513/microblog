# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/2/7 9:44'

from app import db


# 用户类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # 它是被构建成一个 db.relationship 字段。
    # 对于一个一对多的关系，db.relationship 字段通常是定义在“一”这一边。
    posts = db.relationship('Post', backref='author', lazy='dynamic')

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
