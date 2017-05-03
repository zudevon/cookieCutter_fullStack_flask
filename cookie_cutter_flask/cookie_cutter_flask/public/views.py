# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from cookie_cutter_flask.extensions import login_manager
from cookie_cutter_flask.public.forms import LoginForm
from cookie_cutter_flask.user.forms import RegisterForm, ImageCreateForm, ImageDeleteForm, profilePicForm
from cookie_cutter_flask.user.models import User, UserImages, profilePictures
from cookie_cutter_flask.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.me')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/members/')
def members():
    """About page."""
    return render_template('users/members.html')


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)


@blueprint.route('/image/hold/', methods=['GET', 'POST']) #original fuction to create images----
@login_required
def formImage():
    """create Image"""
    form = ImageCreateForm(request.form, csrf_enabled=False)

    if form.validate_on_submit():
        form.create()
        #^^^^^^^^^^add to imgs[].
        flash('Image Created', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
        # 1 retrieve rows from the UserImages
        # User.query.filter(User.filename('user')).all()
        usr_images = UserImages.query.filter(UserImages.user_id == current_user.id)
        # 2 define imgs to be a list of filenames
        imgs = [url_for('static', filename='uploadFolder/' + i.filename) for i in usr_images]

    return render_template('users/image.html', form=form, imgs=imgs)

@blueprint.route('/image/', methods=['GET', 'POST'])# New Function to create Images -------- chnged new HTML
@login_required
def image():
    image_create_form = ImageCreateForm(request.form)
    image_delete_form = ImageDeleteForm(request.form)

    if image_delete_form.validate_on_submit():
        did_delete = image_delete_form.deleteImage()
        if did_delete:
            flash('Image Removed', 'info')
        else:
            flash('Image Doesn\'t Exists', 'error')

    elif image_create_form.validate_on_submit():
        image_create_form.create()
        flash('Image Created', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(image_create_form)
        # 1 retrieve rows from the UserImages
        # User.query.filter(User.filename('user')).all()

    usr_images = UserImages.query.filter(UserImages.user_id == current_user.id)
    # 2 define imgs to be a list of filenames
    # imgs = [url_for('static', filename='uploadFolder/' + i.filename) for i in usr_images]
    image_forms = [ImageDeleteForm(img=i) for i in usr_images]

    return render_template('users/image.html', form=image_create_form, img_forms=image_forms)

@blueprint.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():

    profile_picture_form = profilePicForm(request.form)

    if profile_picture_form.validate_on_submit():
        profile_picture_form.createPP
        flash('Profile Picture Updated', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(profile_picture_form)

    user_pictures = profilePictures.query.filter(profilePictures.filename)
    # profilePictures.create(user_id=cu rrent_user.id, filename=filename)

    # profile_pics = [(img=i) for i in user_pictures]
    return render_template('users/profile.html', form=profile_picture_form, img_forms=user_pictures)  #, img_forms=profile_pics

"""
@blueprint.route('/blogPage/', methods=['GET', 'POST'])
@login_required
def blogPage():

    blogForm = BlogForm(request.form)

"""