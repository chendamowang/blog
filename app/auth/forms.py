# -*- coding: utf-8 -*-
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('保持我的帐号在登录状态')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('[\w\u4e00-\u9fa5]*', 0,
                                          '用户名只包含汉字、字母、数字、下划线 ')])                                          
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='密码必须相同')])
    password2 = PasswordField('重新输入密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('重新输入新密码', validators=[Required()])
    submit = SubmitField('修改密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重设密码')


class PasswordResetForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('重新输入新密码', validators=[Required()])
    submit = SubmitField('重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱地址未知')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('修改邮箱地址')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被注册')
