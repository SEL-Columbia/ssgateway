from webob import Response
from pyramid.view import view_config
from ssgateway.models import DBSession
from ssgateway.models import Meter
from ssgateway.models import User


@view_config(route_name='index', renderer='index.mako', permission='vistor')
def index(request):
    session = DBSession()
    return {'meters': session.query(Meter).all()}


@view_config(route_name='login', renderer='login.mako', permission='vistor')
def login(request):
    return Response()


@view_config(route_name='admin-users', renderer='admin-users.mako')
def admin_user(request):
    session = DBSession()
    return {'users': session.query(User).all()}
