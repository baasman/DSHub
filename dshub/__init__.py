from flask import Flask
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

from .login import setup_login_manager
from .models import db

from config import app_config

login_manager = setup_login_manager()

def create_app(config):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config])
    app.config.from_pyfile('config.py')

    Bootstrap(app)

    login_manager.init_app(app)
    db.init_app(app)

    from dshub.dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    from dshub.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from dshub.project import project as project_blueprint
    app.register_blueprint(project_blueprint)

    from dshub.user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    if app.debug:
        app.config['DEBUG_TB_PANELS'] = (
            'flask_debugtoolbar.panels.versions.VersionDebugPanel',
            'flask_debugtoolbar.panels.timer.TimerDebugPanel',
            'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
            'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
            'flask_debugtoolbar.panels.template.TemplateDebugPanel',
            'flask_debugtoolbar.panels.logger.LoggingPanel',
            'flask_mongoengine.panels.MongoDebugPanel'
        )

        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

        DebugToolbarExtension(app)

    return app