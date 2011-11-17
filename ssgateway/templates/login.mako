<%inherit file="base.mako"/>

<%def name="header()">

</%def>

<%def name="body()">
%for error in errors:

  <span><p>${error}</p></span>
%endfor

<form method="POST" class="" action="${request.route_url('login')}">

  <input type="hidden" name="came_from" value="${came_from}" />
  <div class="clearfix">
    <label>Username</label>
    <div class="input">
      <input class="xlarge" type="text" value="${name}" name="name" placeholder="Username" />
    </div>
  </div>
  <div class="clearfix">
    <label>Password</label>
    <div class="input">
      <input class="xlarge" type="password" name="password" value="" placeholder="Password" />
    </div>
  </div>


  <button type="submit" class="btn">Sign in</button>
</form>

</%def>
