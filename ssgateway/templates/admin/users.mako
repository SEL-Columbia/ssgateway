<%inherit file="../base.mako"/>

<%def name="header()">

</%def>

<%def name="body()">

<div class="well">
  <a class="btn" href="${request.route_url('new-user')}">Add a new user</a>
  <a class="btn" href="${request.route_url('new-group')}">Add a new group</a>
</div>


<table class="zebra-striped bordered-table">
  <thead>
    <td><strong>User name</strong></td>
    <td><strong>User email</strong></td>
    <td><strong>User admin level<strong></td>
  </thead>
  <tbody>
    %for user in users:
    <tr>
      <td><a href="${request.route_url('edit-user', user=user.id)}">
	  ${user.name}</a></td>
      <td>${user.email}</td>
      <td>${user.group}</td>
    </tr>
    %endfor  
  </tbody>
</table>
</%def>
