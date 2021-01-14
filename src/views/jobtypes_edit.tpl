<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
  <meta charset="utf-8">
  <title>Invoice Tracker</title>
  <style>
    form {
      max-width: 500px;
      display: block;
      margin: 1 auto;
    }

    .form-group.required .control-label:after {
      content: "*";
      color: red;
    }
  </style>
</head>

<body>
  % include('base.tpl')
  <header>
    <div class="container">

      % if jobtype:
      <h1 class="logo">Edit Jobtype "{{jobtype.name}}"</h1>
      <form class="p-3" method="post" action="/jobtype_edit/{{jobtype.id}}">
        % else:
        <h1 class="logo">Add New Jobtype</h1>
        <form class="p-3" method="post" action="/jobtype_add">
          % end

          <div class="form-group">
            <b><label class='control-label' for="fname">Jobtype:</label></b>
            % if jobtype:
            <input type="text" id="name" class="form-control" name="name" value="{{jobtype.name}}">
            % else:
            <input type="text" id="name" class="form-control" name="name" style="color:#888;" value="Name" onfocus="inputFocus(this)" onblur="inputBlur(this)">
            % end
          </div>


          <input type="submit" class="btn btn-primary" value="Submit">

        </form>
    </div>
  </header>
</body>

<script>
  function inputFocus(i) {
    if (i.value == i.defaultValue) {
      i.value = "";
      i.style.color = "#000";
    }
  }

  function inputBlur(i) {
    if (i.value == "") {
      i.value = i.defaultValue;
      i.style.color = "#888";
    }
  }
</script>

</html>