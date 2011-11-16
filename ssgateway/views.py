from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from ssgateway.forms import GroupForm
from ssgateway.forms import AddUserForm
from ssgateway.forms import AddMeterForm

from ssgateway.models import DBSession
from ssgateway.models import Meter
from ssgateway.models import User
from ssgateway.models import Group


def get_object_or_404(kls, id):
    if id is None:
        raise HTTPNotFound('No id provided')
    session = DBSession()
    obj = session.query(kls).get(id)
    if obj is None:
        raise HTTPNotFound()
    else:
        return obj


@view_config(route_name='index', renderer='index.mako', permission='vistor')
def index(request):
    session = DBSession()
    return {'meters': session.query(Meter).all()}


@view_config(route_name='login', renderer='login.mako', permission='vistor')
def login(request):
    return Response()


@view_config(route_name='admin-users', renderer='admin/users.mako')
def admin_user(request):
    session = DBSession()
    return {'users': session.query(User).all()}


@view_config(route_name='new-user', renderer='admin/new-user.mako')
def new_user(request):
    session = DBSession()
    form = AddUserForm(request.POST)
    form.group_id.choices = [
        [group.id, group.name] for group in session.query(Group).all()]
    if request.method == 'POST' and form.validate():
        group = session.query(Group).get(form.group_id.data)
        user = User(form.name.data, form.password.data, form.email.data, group)
        session.add(user)
        return HTTPFound(location=request.route_url('admin-users'))
    else:
        return {'form': form}


@view_config(route_name='edit-user', renderer='admin/edit-user.mako')
def edit_user(request):
    session = DBSession()
    user = get_object_or_404(User, request.matchdict.get('user'))
    form = AddUserForm(request.POST, obj=user)
    form.group_id.choices = [
        [group.id, group.name] for group in session.query(Group).all()]
    if request.method == 'POST' and form.validate():
        return {}
    else:
        return {'user': user, 'form': form}


@view_config(route_name='new-group',
             renderer='admin/new-group.mako', permission='admin')
def new_group(request):
    session = DBSession()
    form = GroupForm(request.POST)
    if request.method == 'POST' and form.validate():
        group = Group(form.name.data)
        session.add(group)
        return HTTPFound(location=request.route_url('admin-users'))
    else:
        return {'form': form}


@view_config(route_name='list-meters', renderer='list-meters.mako')
def list_metes(request):
    session = DBSession()
    meters = session.query(Meter).all()
    return {'meters': meters}


@view_config(route_name='new-meter', renderer='meter/new.mako')
def new_meter(request):
    form = AddMeterForm(request.POST)
    if request.method == 'POST' and form.validate():
        return Response(form.data)
    else:
        return {'form': form}
