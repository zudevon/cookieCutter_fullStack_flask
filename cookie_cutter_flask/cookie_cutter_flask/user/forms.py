# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField, FileField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from flask_login import current_user
from flask import current_app, render_template
from .models import User, UserImages, profilePictures



class RegisterForm(Form):
    """Register form."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])
    number = StringField('Phone #', validators=[DataRequired(), Length(min=10, max=14)])


    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered')
            return False
        return True


ALLOWED_EXTENSIONS = set(['img', 'jpg', 'jpeg', 'png', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ImageCreateForm(Form):
    """Image form."""
    image = FileField('image')
    UPLOAD_FOLDER = '/Users/a/myProgs/cookie_cutter_flask/cookie_cutter_flask/static/uploadFolder'

    def validate(self):
        """Validate the form."""
        # image = StringField('image', validators=[DataRequired(), Length(min=3, max=25)])

        initial_validation = super(ImageCreateForm, self).validate()
        if not initial_validation:
            return False

        return True

        # return allowed_file(self.image.data)

    def create(self):

        if request.method == 'POST':
            # check if the post request has the file part
            if 'image' not in request.files:
                flash('No image added')
                return redirect(request.url)
            file = request.files['image']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                UserImages.create(user_id=current_user.id, filename=filename)

                return redirect(url_for('public.image', filename=filename))


class ImageDeleteForm(Form):
    """Image form."""
    # initial_validation = FileField('image', validators=[DataRequired()])
    image_url = HiddenField(validators=[DataRequired()])
    filename = HiddenField(validators=[DataRequired()])
    id = HiddenField(validators=[DataRequired()])

    def __init__(self, img=None, *args, **kwargs):
        super(ImageDeleteForm, self).__init__(*args, **kwargs)
        if isinstance(img, UserImages):
            self.filename.data = img.filename
            self.id.data = img.id
            self.image_url.data = url_for('static', filename='uploadFolder/' + self.filename.data)

    def deleteImage(self):

        leImage = UserImages.query.get(self.id.data)
        if leImage is not None:
            leImage.delete()
            return True
        return False


class profilePicForm(Form):
    """Profile Picture form"""


    image = FileField('image')
    PP_FOLDER = '/Users/a/myProgs/cookie_cutter_flask/cookie_cutter_flask/static/profilePics'

    def validate(self):
        """Validate the form."""


        initial_validation = super(profilePicForm, self).validate()
        if not initial_validation:
            return False

        return True

    def createPP(self):


        if request.method == 'POST':
            # check if the post request has the file part
            if 'image' not in request.files:
                flash('No image added')
                return redirect(request.url)
            file = request.files['image']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['PP_FOLDER'], filename)) #Key eror w/ pp folder

                profilePictures.create(user_id=current_user.id, filename=filename)

                return redirect(url_for('user.profile', filename=filename))

"""
class BlogForm(Form):

    userBio = StringField('blogPost', validators=[DataRequired(), Length(min=0, max=1000)])

    def createBlogPost(self):

        BlogPosts.create(user_id=current_user.id, filename=userBio)
        pass"""



