from wtforms import Form
from wtforms import TextField
from wtforms import validators
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import DecimalField


class GroupForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=25)])


class AddUserForm(Form):
    name = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=4, max=25)])
    email = TextField('Email', [])
    group_id = SelectField('Admin group', coerce=int)


class AddMeterForm(Form):
    name = TextField('Meter name')
    phone = TextField('Meter Phone')
    location = TextField('Meter Location')
    battery_capacity = DecimalField('Batter Capacity')
    panel_capacity = DecimalField('Panel Capacity')
    number_of_circuits = DecimalField('Number of circuits')
    emax = DecimalField('Energy max for circuits')
    pmax = DecimalField('Power max for circuits')
    language = SelectField('Default Langauge',
                           choices=(('en', 'English'), ('fr', 'French')))
