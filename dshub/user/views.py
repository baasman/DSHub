from flask import render_template, g, request, redirect, url_for
from flask_login import current_user

from dshub.models import User, Project, ProjectUser

from . import user
from .forms import AddUserForm

@user.route('/add_user', methods=['GET', 'POST'])
def add_user():
    add_form = AddUserForm()
    project = Project.objects(project_name=request.args.get('project_name'))
    if request.method == 'POST' and add_form.validate_on_submit():
        p_user = ProjectUser(username=add_form.username.data,
                             admin=add_form.admin.data,
                             permission_level=add_form.permission.data)
        project.update(add_to_set__users=p_user)
        return redirect(url_for('project.project_page'))
    return render_template('project/add_user.html', form=add_form, project=project,
                           projects=g.projects)
