<%inherit file="../base.mako"/>
<%namespace name="forms" file="../forms.mako"/>

<%def name="header()">
</%def>

<%def name="body()">
<form method="POST" id="" action="${request.route_url('new-user')}">
  ${forms.make_form(form, 'Add a new user')}
</form>
</%def>
