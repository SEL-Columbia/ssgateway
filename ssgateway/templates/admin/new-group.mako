<%inherit file="admin-base.mako"/>

<%def name="header()">

</%def>

<%def name="body()">
<form method="POST" id="" action="${request.route_url('new-group')}">


%if form.name.errors:
   <div class="alert-message block-message error">${form.name.errors[0]}</div>
%endif 
<div class="clearfix">
  ${form.name.label}
  <div class="input">
    ${form.name}
  </div>
</div>
<div class="clearfix">
  <div class="input">
    <input class="btn" type="submit" name="" value="Add a new group" />
  </div>
</div>

</form>


</%def>
