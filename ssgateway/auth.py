from pyramid.security import Allow
from pyramid.security import Everyone


class RootFactory(object):

    __acl__ = [(Allow, Everyone, 'vistor'),
               (Allow, 'view', 'view'),
               (Allow, 'admin', ('admin', 'view'))]

    def __init__(self, request):
        self.request = request


def group_finder(user_id, request):
    """
    """
