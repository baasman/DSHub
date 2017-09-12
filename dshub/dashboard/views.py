from flask import render_template, g
from flask_login import current_user

from . import dashboard
from dshub.models import User, Project

@dashboard.before_app_request
def before_app_request():
    g.projects = Project.objects(users__username=current_user.username)

@dashboard.route('/home')
def dashboard():
    return render_template('dashboard/dashboard.html', projects=g.projects)