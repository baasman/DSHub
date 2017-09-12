from flask import request, render_template, redirect, url_for, flash, g
from flask_login import current_user

from . import project
from .forms import NewProjectForm
from .utils import scaffold_project_folder

from dshub.models import Project, ProjectUser

import datetime


@project.route('/project/<string:project_name>')
def project_page(project_name):
    project = Project.objects(project_name=project_name).first()
    return render_template('project/project_page.html', project=project, projects=g.projects)


@project.route('/new_project', methods=['GET', 'POST'])
def new_project():
    proj_form = NewProjectForm()

    if request.method == 'POST' and proj_form.validate_on_submit():

        p_user = ProjectUser(username=current_user.username,
                                       admin=True,
                                       permission_level=5)
        project = Project(project_name=proj_form.project_name.data,
                          data_folder=proj_form.data_folder.data,
                          project_folder=proj_form.project_folder.data,
                          date_created=datetime.datetime.now())

        try:
            scaffold_project_folder(project_path=project.project_folder,
                                    data_path=project.data_folder,
                                    username=current_user.username)
        except FileExistsError:
            flash('Folder already exists')
            print('Folder already exists')
            return redirect(url_for('project.new_project'))

        project.save()
        project.update(push__users=p_user)
        return redirect(url_for('dashboard.dashboard'))

    return render_template('project/new_project.html', form=proj_form, projects=g.projects)
