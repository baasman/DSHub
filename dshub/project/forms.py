from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo


class NewProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    project_folder = StringField('Project Folder', validators=[DataRequired()])
    data_folder = StringField('Data Folder', validators=[DataRequired()])
    submit = SubmitField('Create Project')

    def validate(self):
        return True
