<%inherit file="base.mako"/>

<%def name="header()">

</%def>

<%def name="body()">
<div class="well">
  <a class="btn" href="${request.route_url('new-meter')}">Add new meter</a>
  <a class="btn" href="">Add new site</a>
</div>

<table class="zebra-striped bordered-table">
  <thead>
    <td>Meter name</td>
    <td>Meter location</td>
    <td>Meter circuit #</td>
    <td>Meter phone #</td>
    <td>Percentage of hours logs received</td>
  </thead>
  <tbody>
    %for meter in meters:
    <tr>
      <td><a href="${request.route_url('show-meter', meter_id=meter.id)}">
	  ${meter.name}</a></td>
      <td>${meter.location}</td>
      <td>${meter.get_circuits().count()}</td>
      <td>${meter.phone}</td>
      <td>${meter.find_meter_uptime()}</td>
    </tr>
    %endfor
  </tbody>
</table>

</%def>
