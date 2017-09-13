import os

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

def get_notebooks(root_path):
    files = []
    workspace = os.listdir(root_path)
    for file in workspace:
        if os.path.splitext(file)[1] == '.ipynb':
            files.append(file)
    return files


def init_git():
    pass