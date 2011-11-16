<%inherit file="../base.mako"/>
<%namespace name="forms" file="../forms.mako"/>
<%def name="header()">
</%def>


<%def name="body()">
${user}
<form method="POST" action="${request.route_url('edit-user', user=user.id)}">
  ${forms.make_form(form, 'Update user information')}
</form>


</%def>
