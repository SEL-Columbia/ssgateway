from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPFound
from deform import Form
from deform import ValidationFailure
import deform
import colander

from ssgateway.models import DBSession
from ssgateway.models import Meter
from ssgateway.models import User
from ssgateway.models import Group


def get_object_or_404(kls, id):
    if id is None:
        raise HTTPNotFound('No id provided look up')
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

    groups = [[group.id, group.name] for group in session.query(Group).all()]

    class UserSchema(colander.MappingSchema):
        name = colander.SchemaNode(colander.String())
        password = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.CheckedPasswordWidget(size=20)
            )
        email = colander.SchemaNode(colander.String())
        group_id = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.SelectWidget(values=groups)
            )

    schema = UserSchema()
    form = Form(schema, buttons=('submit',))

    if request.method == 'POST':
        try:
            data = form.validate(request.POST.items())
            group = session.query(Group).get(data['group_id'])
            user = User(data['name'], data['password'], data['email'], group)
            session.add(user)
            session.flush()
            return HTTPFound(
                location=request.route_url('edit-user', user=user.id))
        except ValidationFailure, e:
            return {'form': e.render()}
    elif request.method == 'GET':
        return {'form': form.render()}
    else:
        return HTTPForbidden()


@view_config(route_name='edit-user', renderer='admin/edit-user.mako')
def edit_user(request):
    user = get_object_or_404(User, request.matchdict.get('user', None))
    return {'user': user }


class GroupSchema(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())


@view_config(route_name='new-group', renderer='admin/new-group.mako')
def new_group(request):
    session = DBSession()
    schema = GroupSchema()
    form = Form(schema, buttons=('submit'))
    if request.method == 'POST':
        try:
            data = form.validate(request.POST.items())
            group = Group(data.values())
            session.add(group)
            session.flush()
            return HTTPFound(location=request.route_url('admin-users'))
        except ValidationFailure, e:
            return {'form': e.render()}
    elif request.method == 'GET':
        return {'form': form.render()}
    else:
        return HTTPForbidden()
