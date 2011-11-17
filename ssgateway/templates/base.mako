
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <link 
       rel="stylesheet" 
       href="${request.application_url}/static/bootstrap/bootstrap.min.css"
       type="text/css" 
       media="screen" />

    <link rel="stylesheet" 
          href="${request.application_url}/static/custom.css" 
          type="text/css" 
          media="screen" />
    
    ${self.header()}
  </head>
  <body>

    <div class="topbar">      
      <div class="fill">
        <div class="container">
          <h3 class="band">
	    <a href="${request.application_url}">Shared Solar Gateway</a></h3>

          <form method="POST" 
		class="pull-right" 
		action="${request.route_url('login')}">
	    <input type="hidden" 
		   name="came_from" 
		   value="${request.current_route_url()}" />
	    <input class="input-small"
		   type="text" 
		   name="name" 
		   placeholder="Username" />
	    <input class="input-small" 
		   type="password" 
		   name="password" 
		   value="" 
		   placeholder="Password" />
	    <button type="submit" class="btn">Sign in</button>
	  </form>
	  </div>
      </div>
    </div>
    <div class="container">
      <div class="content">
        ${self.body()}
      </div>
    </div>
  </body>
</html>
