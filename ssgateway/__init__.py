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

    # admin interface for users
    config.add_route('admin-users', '/admin/users')
    config.add_route('new-user', '/admin/user/new')
    config.add_route('edit-user', '/admin/user/{user}/edit')
    # manage groups
    config.add_route('new-group', '/admin/group/new')

    config.add_route('list-meters', '/list-meters')

    # maybe these should not be the same url's
    config.add_route('new-meter', '/meter/new')
    config.add_route('show-meter', '/meter/{meter_id}')

    config.add_route('list-messages', '/messages/list')
    config.add_route('show-message', '/message/index/{message}')
    config.add_route('meter-messages', '/messages/show')

    # tokens urls.
    config.add_route('make-tokens', '/manage/make_tokens')
    config.add_route('update_tokens', '/manage/update_tokens')
    # end routes

    config.scan()

    # return the wsgi application
    return config.make_wsgi_app()
