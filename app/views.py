#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-03 20:32:01
# @Last Modified by:  bwael
# @Last Modified time: 2017-01-10 22:34:34

import datetime
import time
import hashlib

from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, session, \
     url_for, request, g, current_app, make_response

from app.forms import LoginForm, SignUpForm, AboutMeForm, PublishForm, \
    EditProfileForm, CommentForm
from app.models import User, Post, ROLE_USER, ROLE_ADMIN, Role, Comment
from app.utils import PER_PAGE
from app import app, db, lm

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)

@app.route('/follow/<name>')
@login_required
def follow(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('users', user_id=user.id))
    current_user.follow(user)
    flash('You are now following %s.' % name)
    return redirect(url_for('users', user_id=user.id))

@app.route('/unfollow/<name>')
@login_required
def unfollow(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('users', user_id=user.id))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % name)
    return redirect(url_for('users', user_id=user.id))

@app.route('/followers/<name>')
def followers(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='followers', pagination=pagination,
                           follows=follows)


@app.route('/followed-by/<name>')
def followed_by(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='followed_by', pagination=pagination,
                           follows=follows)


@app.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@app.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

@app.route('/edit-profile/<int:user_id>', methods=['GET','POST'])
@login_required
def edit_profile(user_id):
    user = User.query.filter(User.id == user_id).first()

    if not user:
        flash('The user is not exist!')
        return redirect(url_for('edit_profile',user_id = current_user.id))

    if user_id != current_user.id:
        flash('Sorry, you can only edit your own profile!', 'error')
        return redirect(url_for('edit_profile',user_id = current_user.id))

    form = EditProfileForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.avatar_hash= hashlib.md5(
            form.email.data.encode('utf-8')).hexdigest()
        user.location = form.location.data
        user.about_me = form.about_me.data
        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash("Database error!")
            return redirect(url_for("user", user_id=user_id))
        flash("Your profile has been update!")
            #return redirect(url_for("users", user_id=user_id))
    else:
        flash("Sorry, May be your data have some error.")

    form.email.data = user.email
    form.location.data = user.location
    form.about_me.data = user.about_me

    return render_template('edit_profile.html',
                            form = form)
    #return redirect(url_for("users", user_id=user_id))

# @app.route('/user/about-me/<int:user_id>', methods=["POST", "GET"])
# @login_required
# def about_me(user_id):
#     user = User.query.filter(User.id == user_id).first()
#     if request.method == "POST":
#         content = request.form.get("describe")
#         if len(content) and len(content) <= 140:
#             user.about_me = content
#             try:
#                 db.session.add(user)
#                 db.session.commit()
#             except:
#                 flash("Database error!")
#                 return redirect(url_for("users", user_id=user_id))
#         else:
#             flash("Sorry, May be your data have some error.")
#     return redirect(url_for("users", user_id=user_id))

@app.route('/publish/<int:user_id>', methods = ['POST', 'GET'])
@login_required
def publish(user_id):
    form = PublishForm()
    posts = Post()

    if user_id != current_user.id:
        flash('Sorry, you can only edit your publish!', 'error')
        return redirect(url_for('index'))

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

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PublishForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('users', user_id=current_user.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@app.route('/user/<int:user_id>', methods = ['GET', 'POST'])
#@app.route('/user/<int:user_id>/page/<int:page>', methods = ['GET', 'POST'])
@login_required
def users(user_id):
    #form = AboutMeForm()
    user = User.query.filter_by(id = user_id).first()
    #blogs = user.posts.paginate(1, PER_PAGE, False).items

    #使用模板的404.html
    if user is None:
        #abort(404)
        flash('The user is not exist!')
        return render_template('404.html')
    #blogs = user.posts.all()

    # if user_id != current_user.id:
    #     flash('Sorry, you can only view your profile!', 'error')
    #     return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    blogs = pagination.items
    # pagination = Post.query.filter_by(
    #     user_id = current_user.id
    #     ).order_by(
    #     db.desc(Post.timestamp)
    #     ).paginate(page, PER_PAGE, False)

    #blogs = user.posts.all()


    return render_template(
        'user.html',
        #form = form,
        user = user,
        posts = blogs,
        pagination = pagination)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email = form.user_email.data,
                    name = form.user_name.data,
                    password = form.password.data)
                    #role = ROLE_USER)
                    #role_id = ROLE_USER)

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
    current_user.ping()
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/login', methods = ['GET','POST'])
def login():
    #验证用户是否已经通过验证
    if current_user.is_authenticated:
        current_user.ping()
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

        # flash('Login request for Name:' + form.name.data)
        # flash('passwd:' + str(form.password.data))
        # flash('remember_me:' + str(form.remember_me.data))
        # return redirect('/index')
    return render_template("login.html",
                            title = 'Log In',
                            form = form)

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
def index():
    form = PublishForm()
    user = None
    show_followed = False
    #验证用户是否已经通过验证
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
        user = User.query.filter(User.id == current_user.id).first()
        if form.validate_on_submit():
            post = Post(body=form.body.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    #posts = Post.query.order_by(Post.timestamp.desc()).all()

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


    #分页显示博客文章列表
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    return render_template("index.html",
                            title = 'Home',
                            form = form,
                            user = user,
                            posts = posts,
                            pagination=pagination,
                            show_followed = show_followed)


