from webob import Response
from pyramid.view import view_config

from ssgateway.models import DBSession
from ssgateway.models import Meter

@view_config(route_name='index', renderer='index.mako', permission='vistor')
def index(request):
    return Response('hello')
