#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-03 20:32:01
# @Last Modified by:  bwael
# @Last Modified time: 2017-01-07 17:47:07

import datetime
import time

from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, session, url_for, request, g

from app.forms import LoginForm, SignUpForm, AboutMeForm, PublishForm
from app.models import User, Post, ROLE_USER, ROLE_ADMIN
from app.utils import PER_PAGE
from app import app, db, lm

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/user/about-me/<int:user_id>', methods=["POST", "GET"])
@login_required
def about_me(user_id):
    user = User.query.filter(User.id == user_id).first()
    if request.method == "POST":
        content = request.form.get("describe")
        if len(content) and len(content) <= 140:
            user.about_me = content
            try:
                db.session.add(user)
                db.session.commit()
            except:
                flash("Database error!")
                return redirect(url_for("users", user_id=user_id))
        else:
            flash("Sorry, May be your data have some error.")
    return redirect(url_for("users", user_id=user_id))

@app.route('/publish/<int:user_id>', methods = ['POST', 'GET' ])
@login_required
def publish(user_id):
    form = PublishForm()
    posts = Post()
    if form.validate_on_submit():
        blog_body = request.form.get('body')
        if not len(blog_body.strip()):
            flash("The content is necessray!")
            return redirect(url_for('publish', user_id = user_id))
        posts.body = blog_body
        posts.timestamp = datetime.datetime.now()
        posts.user_id = user_id

        try:
            db.session.add(posts)
            db.session.commit()
        except:
            flash('Database error!')
            return redirect(url_for('publish', user_id = user_id))

        flash('Publish Successful!')
        return redirect(url_for('publish', user_id = user_id))

    return render_template('publish.html',
                            form = form)

@app.route('/user/<int:user_id>',defaults = {'page':1}, methods = ['GET', 'POST'])
@app.route('/user/<int:user_id>/page/<int:page>', methods = ['GET', 'POST'])
@login_required
def users(user_id, page):
    form = AboutMeForm()
    user = User.query.filter(User.id == user_id).first()
    #blogs = user.posts.paginate(1, PER_PAGE, False).items

    if not user:
        flash('The user is not exist!')
        return redirect(url_for('index'))
    #blogs = user.posts.all()

    if user_id != current_user.id:
        flash('Sorry, you can only view your profile!', 'error')
        return redirect(url_for('index'))


    pagination = Post.query.filter_by(
        user_id = current_user.id
        ).order_by(
        db.desc(Post.timestamp)
        ).paginate(page, PER_PAGE, False)

    #blogs = pagination.items
    blogs = user.posts.all()

    return render_template(
        'user.html',
        form = form,
        user = user,
        blogs = blogs)
        #pagination = pagination)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email = form.user_email.data,
                    name = form.user_name.data,
                    password = form.password.data,
                    role = ROLE_USER)

        #user_name = request.form.get('user_name')
        #user_email = request.form.get('user_email')

        # register_check = User.query.filter(db.or_(
        #     User.nickname == user_name, User.email == user_email)).first()
        # if register_check:
        #     flash("error: The user's name or email already exists!")
        #     return redirect('/sign-up')

        #复查
        # if len(user_name) and len(user_email) and len(password):
        #     user.name = user_name
        #     user.email = user_email
        #     user.password = password
        #     user.role = ROLE_USER
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash("The Database error!")
            return redirect('/sign-up')

        flash("Sign up successful! You can login now.")
        return redirect('/login')

    return render_template(
        "sign_up.html",
        form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/login', methods = ['GET','POST'])
def login():
    #验证用户是否已经通过验证
    if current_user.is_authenticated:
        return redirect('index')
    #登陆验证
    form = LoginForm()
    if form.validate_on_submit():
        user = User.login_check(request.form.get('user_name'))
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
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
            flash('Login failed, Invalid username or password')
            return redirect('/login')

        '''flash('Login request for Name:' + form.name.data)
        flash('passwd:' + str(form.password.data))
        flash('remember_me:' + str(form.remember_me.data))
        return redirect('/index')'''
    return render_template("login.html",
                            title = 'Log In',
                            form = form)

@app.route('/')
@app.route('/index')
def index():

    # user = 'bwael'
    # #user = { 'nickname': 'Miguel' } # 用户名
    # posts = [ #用于提交内容
    # {
    #     'author':{'nickname':'John'},
    #     'body':'Beautiful day in Xi\'an'
    # },
    # {
    #     'author':{'nickname':'Susan'},
    #     'body':'The Avangers movie was so cool'
    # }
    # ]
    # return render_template("index.html",
    #                         title = 'Home',
    #                         user = user,
    #                         posts = posts)

    #
    posts = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template("index.html",
                             title = 'Home',
                             posts = posts
                             )


