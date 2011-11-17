import simplejson
from pyramid.view import view_config
from pyramid.response import Response

from ssgateway.models import DBSession
from ssgateway.models import TokenBatch
from ssgateway.models import Device
from ssgateway.models import Token
from ssgateway.models import Circuit
from ssgateway.models import AddCredit


@view_config(route_name='make-tokens')
def make_tokens(request):
    """
    A view function that allows the vendor application to request to
    new tokens.
    """
    session = DBSession()
    batch = TokenBatch()
    session.add(batch)
    session.flush()
    data = simplejson.loads(request.body)
    if not 'device_id' in data:
        return Response('You must provide an device_id')
    else:
        device = session.query(Device)\
            .filter_by(device_id=data['device_id']).first()
        if device:
            if not 'tokens' in data:
                return Response('You must provide an amount of tokens')
            for group in data['tokens']:
                for i in range(0, group['count']):
                    token = Token(Token.get_random(),
                                  batch=batch,
                                  value=group['denomination'])
                    session.add(token)
                    session.flush()
            return Response(
                [{'token_id': int(token.token),
                  'denomination':
                  float(token.value)} for token in batch.getTokens()])
        else:
            return Response('Not a valid device')


@view_config(route_name='update_tokens')
def update_tokens(request):
    """
    We need to record these updates to token states and provide a
    way to view this in the Gateway Interface.
    """
    session = DBSession()
    data = simplejson.loads(request.body)
    if not 'device_id' in data:
        return Response('You must provide an device_id')
    device = session.query(Device)\
        .filter_by(device_id=data['device_id']).first()
    if device:
        for i in data['tokens']:
            token = session.query(Token)\
                .filter_by(token=i['token_id']).first()
            if token:
                circuit = session.query(Circuit)\
                    .filter_by(pin=i['account_id'])
                if circuit:
                    job = AddCredit(token.value, circuit, token)
                    session.add(job)
                token.state = 5
                session.merge(token)
        session.flush()
        return Response('Ok')
    else:
        return Response('You must provide a valid device_id')
