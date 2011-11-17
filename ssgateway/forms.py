from wtforms import Form
from wtforms import TextField
from wtforms import validators
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class GroupForm(Form):
    """
    The Group form allows users to add Groups via the Gateway UI.
    """
    name = TextField('Name', [validators.Length(min=4, max=25)])


class AddUserForm(Form):
    """
    This form allows users to be added to that Gateway's database.
    """
    name = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=4, max=25)])
    email = TextField('Email', [])
    group = QuerySelectField(get_label='name')


class EditUserForm(Form):
    """
    TODO, Do we need this form?
    """
    name = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email', [])
    group = QuerySelectField(get_label='name')


class AddMeterForm(Form):
    """
    This form allows users to add a new Meter to the Gateway's
    database.  It includes populating the circuits assoicated with an
    meter so the user does not have to add each circuit.
    """
    name = TextField('Meter name', [validators.Length(min=4, max=25)])
    phone = TextField('Meter Phone', [validators.Length(min=4, max=25)])
    location = TextField('Meter Location', [validators.Length(min=4, max=25)])
    battery_capacity = DecimalField('Batter Capacity')
    panel_capacity = DecimalField('Panel Capacity')
    time_zone = QuerySelectField(get_label='zone')
    number_of_circuits = DecimalField('Number of circuits')
    emax = DecimalField('Energy max for circuits')
    pmax = DecimalField('Power max for circuits')
    language = SelectField('Default Langauge',
                           choices=(('en', 'English'), ('fr', 'French')))
