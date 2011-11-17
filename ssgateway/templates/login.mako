<%inherit file="base.mako"/>

<%def name="header()">

</%def>

<%def name="body()">
%for error in errors:
   <p>${error}</p>
%endfor

<form method="POST" class="" action="${request.route_url('login')}">

  <input type="hidden" name="came_from" value="${came_from}" />
  <div class="clearfix">
    <input class="" type="text" value="${name}" name="name" placeholder="Username" />
  </div>
  <div class="clearfix">
    <input class="" type="password" name="password" value="" placeholder="Password" />
  </div>


  <button type="submit" class="btn">Sign in</button>
</form>

</%def>
