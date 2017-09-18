import os
import ntpath

from git import Repo
from flask import current_app as capp


def scaffold_project_folder(project_path, data_path, username):
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    else:
        raise FileExistsError

    if not os.path.exists(data_path):
        os.mkdir(data_path)
    else:
        raise FileExistsError

    for folder in ['validation', 'models', 'workspace']:
        os.mkdir(os.path.join(project_path, folder))

    os.mkdir(os.path.join(project_path, 'workspace', username))
    os.mkdir(os.path.join(project_path, 'workspace', 'shared'))
    os.mkdir(os.path.join(project_path, 'workspace', '.dshub-meta'))



def get_models(root_path):
    model_dir = os.listdir(os.path.join(root_path, 'models'))


def get_notebooks(path):
    f = {}
    f['root'] = []
    dirs = [i for i in os.listdir(path) if i[0] != '.']
    for dir in dirs:
        p_file = os.path.join(path, dir)
        if os.path.isdir(p_file):
            f[dir] = []
            for file in os.listdir(p_file):
                if os.path.splitext(file)[1] == '.ipynb':
                    f[dir].append(file)
        else:
            if os.path.splitext(file)[1] == '.ipynb':
                f['root'].append(ntpath.basename(p_file))
    return f


def get_file_prev_commit(root_path, file_name):

    repo = Repo(root_path)
    index = repo.index
    branch = repo.active_branch

    for file, v in index.entries.items():
        if file[0] == file_name:
            current_entry = (file, v)
            break

    commits = list(repo.iter_commits(branch.name))
    c = commits[0]
    for entry in c.tree.traverse():
        if entry.path == current_entry[0][0]:
            prev_file = entry
            break

    file_content = repo.git.show('{}:{}'.format(c.hexsha, prev_file.path))

    with open(os.path.join(capp.static_folder, 'temp', 'tmp_notebook.ipynb'), 'w') as f:
        f.write(file_content)

def get_prev_commits(repo, branch, file_name):
    commits_touching_path = list(repo.iter_commits(branch, paths=file_name))
    return commits_touching_path