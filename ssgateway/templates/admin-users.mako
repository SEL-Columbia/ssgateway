<%inherit file="base.mako"/>

<%def name="header()">

</%def>

<%def name="body()">

<table>
  <thead>
    <td>User name</td>  
  </thead>
  <tbody>
    %for user in users:
    <tr>
      <td>${user.name}</td>
    </tr>
    %endfor  
  </tbody>
</table>
</%def>
