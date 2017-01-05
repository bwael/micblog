#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-03 20:32:01
# @Last Modified by:  bwael
# @Last Modified time: 2017-01-05 09:57:06

import datetime

from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, session, url_for, request, g

from app.forms import LoginForm, SignUpForm, AboutMeForm
from app.models import User, Post, ROLE_USER, ROLE_ADMIN
from app import app, db, lm

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/user/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def users(user_id):
    form = AboutMeForm()
    user = User.query.filter(User.id == user_id).first()
    if not user:
        flash('The user is not exist!')
        redirect('/index')
    blogs = user.post.all()

    return render_template(
        'user.html',
        form = form,
        user = user)
        blogs = blogs)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    user = User()
    if form.validate_on_submit():
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')

        register_check = User.query.filter(db.or_(
            User.nickname == user_name, User.email == user_email)).first()
        if register_check:
            flash("error: The user's name or email already exists!")
            return redirect('/sign-up')

        if len(user_name) and len(user_email):
            user.nickname = user_name
            user.email = user_email
            user.role = ROLE_USER
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("The Database error!")
                return redirect('/sign-up')

            flash("Sign up successful!")
            return redirect('/index')

    return render_template(
        "sign_up.html",
        form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods = ['GET','POST'])
def login():
    #验证用户是否已经通过验证
    if current_user.is_authenticated:
        return redirect('index')
    #注册验证
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login_check(request.form.get('user_name'))
        if user:
            login_user(user)
            user.last_seen = datetime.datetime.now()

            try:
                db.session.add(user)
                dn.session.commit()
            except:
                flash('The Database error!')
                redirect('/login')

            flash('Your name: ' + request.form.get('user_name'))
            flash('remember me? ' + str(request.form.get('remember_me')))
            #return redirect(url_for("users", user_id=current_user.id))
            return redirect('/index')
        else:
            flash('Login failed, Your name is not exist!')
            return redirect('/login')

        '''flash('Login request for Name:' + form.name.data)
        flash('passwd:' + str(form.password.data))
        flash('remember_me:' + str(form.remember_me.data))
        return redirect('/index')'''
    return render_template("login.html",
                            title = 'Sign In',
                            form = form)

@app.route('/')
@app.route('/index')
def index():
    user = 'Man'
    #user = { 'nickname': 'Miguel' } # 用户名
    posts = [ #用于提交内容
    {
        'author':{'nickname':'John'},
        'body':'Beautiful day in Xi\'an'
    },
    {
        'author':{'nickname':'Susan'},
        'body':'The Avangers movie was so cool'
    }
    ]
    return render_template("index.html",
                            title = 'Home',
                            user = user,
                            posts = posts)


