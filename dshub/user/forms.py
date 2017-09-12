from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    admin = BooleanField('Admin', validators=[DataRequired])
    permission = IntegerField('Permission Level', validators=[DataRequired])
    submit = SubmitField('Add')

    def validate(self):
        return True