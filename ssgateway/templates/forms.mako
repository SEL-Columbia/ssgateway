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
