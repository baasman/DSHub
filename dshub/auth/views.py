from flask import request, redirect, render_template, url_for
from flask_login import login_user, logout_user, current_user

from . import auth
from .forms import LoginForm, RegistrationForm
from dshub.models import User

import sys


@auth.before_request
def before_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))


@auth.route('/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        user = User.objects(username=login_form.username.data).first()
        if user and user.validate_login(user.password_hash, login_form.password.data):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))

    return render_template('auth/login.html', form=login_form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if request.method == 'POST' and reg_form.validate_on_submit():
        user = User(email=reg_form.email.data,
                    username=reg_form.username.data)
        user.password_hash = user.set_password(reg_form.password.data)
        try:
            user.save()
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        except:
            print(sys.exc_info()[:2])
    return render_template('auth/register.html', form=reg_form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))