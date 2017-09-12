from dshub import create_app

app = create_app('development')


if app.config.get('RUN_LOCAL'):
    app.run(port=8011)