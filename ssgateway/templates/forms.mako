<%def name="make_form(form, button_string)">
 %for field in form:
    %if field.errors:
      <div class="clearfix error">
    %else:
      <div class="clearfix">
    %endif
      <label${field.label}</label>
      <div class="input">
          ${field}
	  %if field.errors:
	     <span class="help-inline">${field.errors[0]}</span>
	  %endif
	</div>
      </div>
 %endfor
<input class="btn" type="submit" name="" value="${button_string}" />
</%def>

<%def name="login_form()">

%if user:
<ul class="nav secondary-nav">
  <li><a href="#">${user}</a></li>
  <li><a href="${request.route_url('logout')}">Log out</a></li>
</ul>
%else:
<form method="POST" class="pull-right" action="${request.route_url('login')}">

  <input type="hidden" name="came_from" value="${request.current_route_url()}" />
  <input class="input-small" type="text" name="name" placeholder="Username" />
  <input class="input-small" type="password" name="password" value="" placeholder="Password" />
  <button type="submit" class="btn">Sign in</button>

</form>

%endif

</%def>
