<%inherit file="base.mako"/>

<%def name="header()">
</%def>

<%def name="body()">
  <a class="btn" href="${request.route_url('admin-users')}">Manage users and groups</a>
</%def>
