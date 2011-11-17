<%namespace name="forms" file="forms.mako"/>
<%namespace name="headers" file="headers.mako"/>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    ${headers.css_links()}
    ${self.header()}
  </head>
  <body>
    <div class="topbar">      
      <div class="fill">
        <div class="container">
          <h3 class="band">
	    <a href="${request.application_url}">Shared Solar Gateway</a></h3>
	    ${forms.login_form()}
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
