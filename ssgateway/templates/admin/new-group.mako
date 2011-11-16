<%inherit file="admin-base.mako"/>
<%namespace name="forms" file="../forms.mako"/>
<%def name="header()">

</%def>

<%def name="body()">
<form method="POST" id="" action="${request.route_url('new-group')}">
${forms.make_form(form, 'Add a new group')}
</form>
</%def>
