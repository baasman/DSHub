from flask import request, render_template, redirect, url_for, flash, g, current_app
from flask_login import current_user

from git import Repo

from . import project
from .forms import NewProjectForm
from .utils import scaffold_project_folder, get_models, get_notebooks, get_prev_commits

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


@project.route('/project/<string:project_name>/notebook/<string:nb_name>', methods=['GET', 'POST'])
def view_notebook(project_name, nb_name):
    # TODO: clean up abysmal view

    project = Project.objects(project_name=project_name).first()
    repo = Repo(project.project_folder)
    current_branch = repo.active_branch

    folder_name = request.args.get('folder_name')
    if folder_name == 'root':
        ipy_file = os.path.join(project.project_folder, 'workspace', nb_name)
        rel_file = os.path.join('workspace', nb_name)
    else:
        ipy_file = os.path.join(project.project_folder, 'workspace', folder_name, nb_name)
        rel_file = os.path.join('workspace', folder_name, nb_name)

    commits = get_prev_commits(repo, current_branch, rel_file)
    all_commits = []
    for commit in commits:
        all_commits.append({'date': commit.committed_datetime,
                            'committer': commit.author,
                            'message': commit.message[:20] + '...',
                            'rel_file': rel_file,
                            'project_folder': project.project_folder})

    nb_to_file = os.path.join(current_app.static_folder, 'notebooks', nb_name).replace('.ipynb', '.html')
    if not os.path.exists(nb_to_file):
        try:
            c = subprocess.check_call('jupyter nbconvert --to html --template full %s' % ipy_file,
                                      shell=True)
        except subprocess.SubprocessError:
            flash('Error converting jupyter notebook')
            return redirect('project.project_page', project_name=project.project_name)

        if c == 0:
            shutil.move(ipy_file.replace('.ipynb', '.html'), nb_to_file)
        else:
            raise Exception
    html_file = ntpath.basename(nb_to_file)

    jupyter = project.jupyter_notebook

    return render_template('project/notebook_view.html', notebook=html_file, projects=g.projects,
                           jupyter=jupyter, commits=all_commits)


@project.route('/notebook_diff')
def notebook_diff():
    rel_file = request.args.get('rel_file')
    project_path = request.args.get('project_folder')
    repo = Repo(project_path)

    # TODO: Use rest api (not frozen yet), not subprocess call
    # full_path = os.path.join(project_path, rel_file)
    # subprocess.Popen('nbdime show %s' % (rel_file), cwd=project_path, shell=True)
    diff = repo.git.diff(rel_file)
    return redirect(url_for('dashboard.dashboard'))



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
            return redirect(url_for('project.new_project'))

        project.save()
        project.update(push__users=p_user)
        return redirect(url_for('dashboard.dashboard'))

    return render_template('project/new_project.html', form=proj_form, projects=g.projects)
