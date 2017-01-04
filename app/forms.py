#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: bwael
# @Date:   2017-01-03 21:55:53
# @Last Modified by:   bwael
# @Last Modified time: 2017-01-04 21:23:51

#from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, TextField, SubmitField
from wtforms.validators import Required, Email, Length


class LoginForm(FlaskForm):
    user_name = TextField('Name', validators=[
        Required(),Length(max = 15)])
    remember_me = BooleanField('Remenber me?', default=False)
    submit = SubmitField('Log in')

class SignUpForm(FlaskForm):
    user_name = TextField('user name', validators=[
        Required(), Length(max=15)])
    user_email = TextField('user email', validators=[
        Email(), Required(), Length(max=128)])
    submit = SubmitField('Sign up')


