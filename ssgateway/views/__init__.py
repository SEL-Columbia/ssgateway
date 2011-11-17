from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ssgateway.forms import GroupForm
from ssgateway.forms import AddMeterForm

from ssgateway.models import DBSession
from ssgateway.models import Meter
from ssgateway.models import Group
from ssgateway.models import TimeZone


@view_config(route_name='index', renderer='index.mako', permission='vistor')
def index(request):
    """
    Main view function for the gateway ui. Currently does very little.
    """
    return {}


@view_config(route_name='new-group',
             renderer='admin/new-group.mako', permission='admin')
def new_group(request):
    """
    A view function to add a new admin group to the Gateway.
    Should removed this because its should not be a public function.
    """
    session = DBSession()
    form = GroupForm(request.POST)
    if request.method == 'POST' and form.validate():
        group = Group(form.name.data)
        session.add(group)
        return HTTPFound(location=request.route_url('admin-users'))
    else:
        return {'form': form}


@view_config(route_name='list-meters', renderer='list-meters.mako')
def list_metes(request):
    """
    Lists all of the active meters currently configure in the
    Gateway. TODO, need to limit this view to only the meters
    associated with a user's org.
    """
    session = DBSession()
    meters = session.query(Meter).all()
    return {'meters': meters}


@view_config(route_name='new-meter', renderer='meter/new.mako')
def new_meter(request):
    """
    View function that allows users to add a new meter to the
    Gateway's database.
    """
    session = DBSession()
    form = AddMeterForm(request.POST)
    form.time_zone.choices = [
        [t.id, t.zone] for t in session.query(TimeZone).all()]
    if request.method == 'POST' and form.validate():
        tz = session.query(TimeZone).get(form.timezone.data)
        meter = Meter(form.name.data,
                      form.phone.data,
                      form.location.data,
                      tz,
                      form.battery_capacity.data,
                      form.panel_capacity)
        # todo, add the assoicated circuits.
        session.add(meter)
        session.flush()
        return Response(form.data)
    else:
        return {'form': form}
