from pyramid_beaker import session_factory_from_settings
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.events import subscriber
from pyramid.events import BeforeRender
from pyramid.threadlocal import get_current_request
from pyramid.security import authenticated_userid

from ssgateway.models import initialize_sql


@subscriber(BeforeRender)
def add_global(event):
    """
    Add the user object to the global env do we don't have to pass a
    user object to each view function.
    From
    http://docs.pylonsproject.org/projects/pyramid/1.2/narr/hooks.html#using-the-before-render-event
    """
    request = event.get('request')
    if request is None:
        request = get_current_request()
    globs = {'user': authenticated_userid(request)}
    event.update(globs)


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
    # manage sites
    config.add_route('list-sites', '/list-sites')
    config.add_route('new-site', '/site/new')

    config.add_route('list-organizations', '/list-organization')
    config.add_route('new-orgainzation', '/organization/new')

    config.add_route('list-countries', '/list-countries')
    config.add_route('new-country', '/country/new')

    # maybe these should not be the same url's
    config.add_route('list-meters', '/list-meters')
    config.add_route('new-meter', '/meter/new')
    config.add_route('show-meter', '/meter/{meter_id}')

    # vendor applications
    config.add_route('list-devices', '/list-devices')
    config.add_route('new-device', '/device/new')

    # tokens urls.
    config.add_route('list-tokens', '/list-tokens')
    config.add_route('make-tokens', '/manage/make_tokens')
    config.add_route('update_tokens', '/manage/update_tokens')
    # message relays
    config.add_route('list-relays', '/list-relays')
    config.add_route('new-relay', '/message-relay/new')

    # messages

    config.add_route('list-messages', '/messages/list')
    config.add_route('show-message', '/message/index/{message}')
    config.add_route('meter-messages', '/messages/show')

    # alerts and alarms
    config.add_route('list-alerts', '/list-alerts')
    config.add_route('send-message', '/send/message')
    config.add_route('check-comm-gaps', '/check-comm-gaps')

    # end routes
    config.scan()

    # return the wsgi application
    return config.make_wsgi_app()
