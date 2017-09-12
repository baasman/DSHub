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
