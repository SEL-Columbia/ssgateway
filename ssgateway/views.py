"""
Views functions for SharedSolar Gateway
"""
from ssgateway.models import DBSession
from ssgateway.models import Meter


def index(request):
    session = DBSession()
    meters = session.query(Meter).all()
    return {'meters': meters}
