from ssgateway.models import DBSession
from ssgateway.models import Meter
from ssgateway.models import PowerOn


def find_meter(func):

    def wrap(message):
        session = DBSession()
        number = message.get('phone-number', None)
        if number:
            meter = session.query(Meter).filter_by(phone=number).first()
        return func(message, meter)
    return wrap


@find_meter
def alert_meter_online(message, meter):
    """
    Function to record when a meter sends a meter online message
    """
    import pdb; pdb.set_trace()
