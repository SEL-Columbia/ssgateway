
from pyramid_beaker import session_factory_from_settings
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from ssgateway.models import initialize_sql


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    initialize_sql(settings.get('sqlalchemy.url'), echo=False)

    #change for a production machine
    authn_policy = AuthTktAuthenticationPolicy('seekrit')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        root_factory='ssgateway.auth.RootFactory',
        authentication_policy=authn_policy,
        authorization_policy=authz_policy
        )

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # add the static url for development
    config.add_static_view('static', 'ssgateway:static')

    # add the routes
    config.add_route('index', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('admin-users', '/admin/users')
    # end routes

    config.scan()

    # return the wsgi application
    return config.make_wsgi_app()
