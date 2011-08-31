from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from ssgateway.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    initialize_sql(settings.get('sqlalchemy.url'), echo=False)

    config = Configurator(settings=settings)

    config.add_static_view('static', 'ssgateway:static')

    config.add_route('home', '/')

    config.add_view('ssgateway.views.index',
                    route_name='home',
                    renderer='index.mako')

    return config.make_wsgi_app()
