# -*- coding:utf-8 -*-


__author__ = 'gjw'
__date__ = '2018/2/7 9:44'

from app import db
from hashlib import md5

# 添加followers表
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


# 用户类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # 它是被构建成一个 db.relationship 字段。
    # 对于一个一对多的关系，db.relationship 字段通常是定义在“一”这一边。
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    # 关注
    followed = db.relationship('User',
                               # 指定关系的辅助表
                               secondary=followers,
                               # 辅助表中连接左边实体(发起关注的用户)的条件
                               primaryjoin=(followers.c.follower_id == id),
                               # 辅助表中连接右边实体(被关注的用户)的条件
                               secondaryjoin=(followers.c.follower_id == id),
                               # 定义这种关系将如何从右边实体进行访问
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    # Flask-Login 扩展需要在我们的 User 类中实现一些特定的方法。
    # 但是类如何去实现这些方法却没有什么要求。

    # # 这个方法应该只返回 True，除非表示用户的对象因为某些原因不允许被认证
    # @property
    # def is_authenticated(self):
    #     return True
    #
    # # is_active方法应该返回True，除非是用户是无效的，比如因为他们的账号是被禁止。
    # @property
    # def is_active(self):
    #     return True
    #
    # # is_anonymous 方法应该返回 True，如果是匿名的用户不允许登录系统。
    # @property
    # def is_anonymous(self):
    #     return False

    is_authenticated = True
    is_active = True
    is_anonymous = False

    # get_id 方法应该返回一个用户唯一的标识符，以 unicode 格式
    def get_id(self):
        return str(self.id)

    # User 的方法 avatar 返回用户图片的 URL，以像素为单位缩放成要求的尺寸。
    def avatar(self, size):
        # hashlib.md5(data)函数中，data参数的类型应该是bytes
        # hash前必须把数据转换成bytes类型
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode("utf-8")).hexdigest() + '?d=mm&s=' + str(size)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first():
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first():
                break
            version += 1
        return new_nickname

    # 关注
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    # 取消关注
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    # 是否关注
    def is_following(self, user):
        return self.followed.filter(followers.c.follower_id == user.id).count() > 0

    # 查询被关注者的blog
    def followed_posts(self):
        # 连接、过滤、排序
        return Post.query.join(followers, (followers.c.follower_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

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
