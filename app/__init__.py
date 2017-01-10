#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-03 20:31:28
# @Last Modified by:   bwael
# @Last Modified time: 2017-01-08 12:43:48

from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
#from .momentjs import momentjs


#初始化flask应用
app = Flask(__name__)
app.config.from_object('config')

#初始化数据库
db = SQLAlchemy(app)

#初始化flask_login
lm = LoginManager()
lm.setup_app(app)

#初始化bootstrap
bootstrap = Bootstrap(app)

#初始化moment
moment = Moment(app)
#app.jinja_env.globals['momentjs'] = momentjs

from app import views, models