# -*- coding:utf-8 -*-
__author__ = 'gjw'
__date__ = '2018/2/6 10:47'

import os
# 激活跨站点请求伪造
CSRF_ENABLED = True
# 上面的参数必须激活
# 建立一个加密的令牌，用于验证表单
SECRET_KEY = 'you-will-never-guess'

# openid提供者
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]



