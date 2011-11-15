<!DOCTYPE html>
<html lang="en">
  <head>
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
      <div class="topbar-inner">
        <div class="container">
          <h1><a href="${request.application_url}">Shared Solar Gateway</a></h1>
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
