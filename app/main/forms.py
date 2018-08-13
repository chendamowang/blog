# -*- coding: utf-8 -*-
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, FileField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_wtf.file import FileAllowed
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('你叫什么名字？', validators=[Required()])
    submit = SubmitField('提交')

class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[Length(0, 64)])
    avatar = FileField('头像',validators=[FileAllowed(['jpg', 'png', 'gif'], '文件格式不符合')])
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit =SubmitField('提交')
    
    #def validate_avatar(self, field):
        #avatar = request.files['avatar']
        ##fname = avatar.filename
        #ALLOWER_EXTENSIONS = ['png','jpg','jpeg','gif']
        #flag = '.' in fname and fname.split('.')[1] in ALLOWER_EXTENSIONS
        #if not flag:
       #     raise ValidationError('文件类型不符合')

class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('[\w\u4e00-\u9fa5]*', 0,
                                          '用户名只包含汉字、字母、数字、下划线 ')])                                          
    confirmed = BooleanField('确认')
    role = SelectField('角色', coerce=int)
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit =SubmitField('提交')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user
    
    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('此邮箱已被注册')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用')

class PostForm(FlaskForm):
    body = PageDownField('你在想什么呢？', validators=[Required()])
    submit = SubmitField('提交')
   
