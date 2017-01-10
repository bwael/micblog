#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-03 21:55:53
# @Last Modified by:   bwael
# @Last Modified time: 2017-01-10 22:17:24

#from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, TextField, SubmitField,\
         TextAreaField, StringField
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms import ValidationError

from app.models import User

class CommentForm(FlaskForm):
    body = StringField('', validators = [Required()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    user_name = TextField('Name', validators=[
        Required(),Length(max = 15)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Remember me?', default=False)
    submit = SubmitField('Log in')

class SignUpForm(FlaskForm):
    user_name = TextField('user name', validators=[
        Required(), Length(max=15)])
    user_email = TextField('user email', validators=[
        Email(), Required(), Length(max=128)])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message = 'Password must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Sign up')

    def validate_user_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already exists.')

    def validate_user_name(self, field):
        if User.query.filter_by(name = field.data).first():
            raise ValidationError('Username already exists.')

class AboutMeForm(FlaskForm):
    describe = TextAreaField('about me', validators=[
        Required(), Length(max=140)])
    submit = SubmitField('Yes!')

class PublishForm(FlaskForm):
    body = TextAreaField('What\'s on your mind?', validators = [Required()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators = [
        Email(), Required(), Length(max=120)])
    location = StringField('Location', validators = [Length(0, 64)])
    about_me = TextAreaField('About me', validators=[
        Required(), Length(max=140)])
    submit = SubmitField('Yes!')

    def validate_user_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already exists.')

