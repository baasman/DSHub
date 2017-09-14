import os
import ntpath

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


def init_git():
    pass