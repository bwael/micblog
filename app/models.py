#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-04 20:49:12
# @Last Modified by:   bwael
# @Last Modified time: 2017-01-08 12:51:03

from datetime import datetime

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin, login_manager

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    #每个属性定义一个字段
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    #role = db.Column(db.SmallInteger, default = ROLE_USER)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    location = db.Column(db.String(64))
    about_me = db.Column(db.String(140))
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def login_check(cls, user_name):
        user = cls.query.filter(db.or_(
            User.name == user_name, User.email == user_name
        )).first()
        if not user:
            return None

        return user

    # 用于记录上一次登陆时间
    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == current_app.config['FLASKY_ADMIN']:
    #             self.role = Role.query.filter_by(permissions=0xff).first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

class Permission:
    FOLLOW = 0x01 #关注用户
    COMMENT = 0x02 #发表评论
    WRITE_ARTICLES = 0x04 #写文章
    MODERATE_COMMENTS = 0x08 #管理他人评论
    ADMINISTER = 0x80 #管理员

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name



