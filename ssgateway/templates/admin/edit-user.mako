<%inherit file="../base.mako"/>
<%namespace name="forms" file="../forms.mako"/>
<%def name="header()">
</%def>


<%def name="body()">
${user}
${forms.make_form(form, 'Update user information')}

</%def>
