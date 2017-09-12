from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

db = MongoEngine()

# User
class UserProject(db.EmbeddedDocument):
    project_name = db.StringField(unique=True)
    date_joined = db.DateTimeField()


class User(db.Document):

    username = db.StringField(required=True, primary_key=True)
    password_hash = db.StringField()
    email = db.StringField(unique=True)
    admin = db.BooleanField(default=False)

    projects = db.ListField(db.EmbeddedDocumentField(UserProject))

    date_joined = db.DateTimeField()

    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    def set_password(self, password):
        return generate_password_hash(password)


# Project

class ProjectUser(db.EmbeddedDocument):
    username = db.StringField()
    admin = db.BooleanField(default=False)
    permission_level = db.IntField()


class Project(db.Document):

    project_name = db.StringField(primary_key=True)
    project_folder = db.StringField()
    data_folder = db.StringField()

    models = db.ListField(db.IntField())

    users = db.ListField(db.EmbeddedDocumentField(ProjectUser))
    github_remote = db.StringField()
    local_git = db.ListField(db.StringField())

    date_created = db.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return 'project=%s' % self.project_name


# Model

class Model(db.Document):

    model_id = db.IntField(primary_key=True)
    model_name = db.StringField()
    version = db.StringField()
    file_path = db.StringField()
    part_of = db.StringField()
