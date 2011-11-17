<%inherit file="base.mako"/>

<%def name="header()">
</%def>

<%def name="body()">

<div class="well">
  <h3>Meter, circuits and tokens</h3>
  <a class="btn" href="${request.route_url('list-meters')}">Manage meters</a>
  <a class="btn" href="${request.route_url('list-devices')}">Manage devices (Vendor tablets)</a>
  <a class="btn" href="${request.route_url('list-tokens')}">Manage tokens</a>
</div>

<div class="well">
  <h3>Messages, alerts and alarms</h3>
  <a class="btn" href="${request.route_url('new-relay')}">Manage message relays</a>
  <a class="btn" href="${request.route_url('list-messages')}">List all SMS messages</a>
  <a class="btn" href="${request.route_url('meter-messages')}">List all meter messages</a>
  
</div>

<div class="well">
  <h3>Users and organizations</h3>
  <a class="btn" href="${request.route_url('admin-users')}">Manage users</a> 

  <a class="btn" href="${request.route_url('list-organizations')}">Manage organizations</a>

</div>


</%def>
