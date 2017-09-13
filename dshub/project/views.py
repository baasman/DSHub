from flask import request, render_template, redirect, url_for, flash, g, current_app
from flask_login import current_user

from . import project
from .forms import NewProjectForm
from .utils import scaffold_project_folder, get_models, get_notebooks

from dshub.models import Project, ProjectUser

import datetime
import os
import shutil
import ntpath
import subprocess

@project.route('/project/<string:project_name>')
def project_page(project_name):
    project = Project.objects(project_name=project_name).first()
    notebooks = {'ws': get_notebooks(os.path.join(project.project_folder, 'workspace')),
                 'm': [],
                 'v': []}
    return render_template('project/project_page.html', project=project, projects=g.projects,
                           notebooks=notebooks)


@project.route('/project/<string:project_name>/notebook/<string:nb_name>')
def view_notebook(project_name, nb_name):
    project = Project.objects(project_name=project_name).first()

    ipy_file = os.path.join(project.project_folder, 'workspace', nb_name)

    nb_to_file = os.path.join(current_app.static_folder, 'notebooks', nb_name).replace('.ipynb', '.html')
    if not os.path.exists(nb_to_file):
        c = subprocess.check_call('jupyter nbconvert --to html --template full %s' % ipy_file,
                                  shell=True)
        if c == 0:
            shutil.copyfile(ipy_file.replace('.ipynb', '.html'), nb_to_file)
        else:
            raise Exception
    html_file = ntpath.basename(nb_to_file)

    return render_template('project/notebook_view.html', notebook=html_file, projects=g.projects)


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
