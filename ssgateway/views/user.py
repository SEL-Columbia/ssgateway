
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget
import hashlib

from ssgateway.forms import AddUserForm
from ssgateway.forms import EditUserForm
from ssgateway.models import DBSession
from ssgateway.models import User
from ssgateway.models import Group
from ssgateway.views.utils import get_object_or_404


@view_config(route_name='login', renderer='login.mako', permission='vistor')
def login(request):
    """
    View function to allow users to log into the Gateway auth's
    system. Checks the sanity of the user's input and then makes sure
    that we have a the user in the database.

    Returns a HTTPFound to the user's last url.
    """
    session = DBSession()
    came_from = request.params.get('came_from', '/')
    errors = ''
    name = ''
    if 'form.submitted' in request.params:
        name = request.params['name']
        # consume the user's password and convert it to a md5 hash
        # which we use to check against the database.
        password = hashlib.md5(request.params['password']).hexdigest()
        # query the database making sure that a user with both the
        # username and password exists.
        user = session.query(User)\
            .filter_by(name=name)\
            .filter_by(password=password).first()
        # if we have a user, send them on their way.
        # else allow them to try again.
        if user is not None:
            headers = remember(request, user.name)
            return HTTPFound(
                location=came_from,
                headers=headers
                )
        errors = u'Unable to log in, please try again'
    return {'errors': errors, 'name': name}


@view_config(route_name='logout')
def logout(request):
    """
    View function that allows users to log out of the Gateway.
    Returns the user to the home page of the Gateway.
    """
    headers = forget(request)
    return HTTPFound(
        headers=headers,
        location=request.application_url
        )


@view_config(route_name='edit-user', renderer='admin/edit-user.mako')
def edit_user(request):
    """
    Allows a user to edit the profile. This should be limited...
    """
    session = DBSession()
    user = get_object_or_404(User, request.matchdict.get('user'))
    form = EditUserForm(request.POST, obj=user)
    form.group.query = session.query(Group).all()
    if request.method == 'POST' and form.validate():
        group = session.query(Group).get(form.group_id.data)
        user.name = form.name.data
        user.email = form.email.data
        user.group = group
        session.merge(user)
        return HTTPFound(location=request.route_url('admin-users'))
    else:
        return {'user': user, 'form': form}


@view_config(route_name='admin-users', renderer='admin/users.mako')
def admin_user(request):
    """
    Function that displays the main user admin interface of the
    Gateway.  Right now displays a list of all the users and gives the
    user the option to add a new user.
    """
    session = DBSession()
    return {'users': session.query(User).all()}


@view_config(route_name='new-user', renderer='admin/new-user.mako')
def new_user(request):
    """
    Function to add a new user to the Gateway's auth system.
    Requires the user to provide a user name, password and email address.
    The group for the new user is give a list to select from.

    TODO, add support for org's once they are add to the models.
    """
    session = DBSession()
    form = AddUserForm(request.POST)
    form.group.query = session.query(Group).all()
    if request.method == 'POST' and form.validate():
        user = User(form.name.data,
                    form.password.data,
                    form.email.data,
                    form.group.data)
        session.add(user)
        return HTTPFound(location=request.route_url('admin-users'))
    else:
        return {'form': form}
