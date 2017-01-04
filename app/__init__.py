#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-03 20:31:28
# @Last Modified by:   bwael
# @Last Modified time: 2017-01-04 21:14:25

from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


#初始化flask应用
app = Flask(__name__)
app.config.from_object('config')

#初始化数据库
db = SQLAlchemy(app)

#初始化flask_login
lm = LoginManager()
lm.setup_app(app)

from app import views, models