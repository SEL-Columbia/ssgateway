from wtforms import Form
from wtforms import TextField
from wtforms import validators
from wtforms import PasswordField
from wtforms import SelectField


class GroupForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=25)])


class AddUserForm(Form):
    name = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=4, max=25)])
    email = TextField('Email', [])
    group_id = SelectField('Admin group', coerce=int)
    
