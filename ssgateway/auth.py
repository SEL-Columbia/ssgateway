from pyramid.security import Allow
from pyramid.security import Everyone

from ssgateway.models import User
from ssgateway.models import DBSession


class RootFactory(object):

    __acl__ = [(Allow, Everyone, 'vistor'),
               (Allow, 'view', 'view'),
               (Allow, 'admin', ('admin', 'view'))]

    def __init__(self, request):
        self.request = request


def group_finder(user_id, request):
    """
    """
    session = DBSession()
    user = session.query(User).filter_by(name=user_id).first()
    if user:
        if user.group:
            return [user.group.name]
