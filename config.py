#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-03 21:55:53
# @Last Modified by:   bwael
# @Last Modified time: 2017-01-04 21:08:22

#sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'venv/Lib/site-packages'))

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'bwael'