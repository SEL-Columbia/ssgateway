<%inherit file="base.mako"/>

<%def name="header()">
</%def>

<%def name="body()">
<div class="well">
  <a class="btn" 
     href="${request.route_url('admin-users')}">Manage users and groups</a>  
  <a class="btn"
     href="${request.route_url('list-meters')}">Manage meters</a>
</div>



</%def>
