from datetime import datetime
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from ssgateway.forms import GroupForm
from ssgateway.forms import AddMeterForm

from ssgateway.models import DBSession
from ssgateway.models import Meter
from ssgateway.models import Group
from ssgateway.models import TimeZone
from ssgateway.models import Circuit
from ssgateway.models import Account
from ssgateway.views.utils import process_form


@view_config(route_name='index', renderer='index.mako', permission='vistor')
def index(request):
    """
    Main view function for the gateway ui. Currently does very little.
    """
    return {}


@view_config(route_name='new-group', renderer='admin/new-group.mako',)
def new_group(request):
    """
    A view function to add a new admin group to the Gateway.
    Should removed this because its should not be a public function.
    """
    session = DBSession()
    form = GroupForm(request.POST)

    def post_validate(form):
        group = Group(form.name.data)
        session.add(group)
        return HTTPFound(location=request.route_url('admin-users'))
    return process_form(request, form, post_validate)


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
    form.time_zone.query = session.query(TimeZone).all()

    def post_validate(form):
        meter = Meter(form.name.data,
                      form.phone.data,
                      form.location.data,
                      form.time_zone.data,
                      True,
                      datetime.now(),
                      form.battery_capacity.data,
                      form.panel_capacity.data)
        session.add(meter)
        start_ip_address = 200
        for x in range(0, int(form.number_of_circuits.data)):
            ip_address = '192.168.1.%s' % (start_ip_address + x)
            # create an account for each circuit
            account = Account('default-account', '', form.language.data)
            session.add(account)
            # create the circuit
            circuit = Circuit(
                meter,
                account,
                datetime.now(),
                Circuit.get_pin(),
                form.pmax.data,
                form.emax.data,
                ip_address,
                0,
                0)
            session.add(circuit)
        # flush the session so i can send the user to the meter's id
        session.flush()
        return HTTPFound(
            location=request.route_url('show-meter', meter_id=meter.id)
            )
    return process_form(request, form, post_validate)
