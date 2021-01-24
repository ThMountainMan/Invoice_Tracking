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

    .form-group.required .control-label:before {
      color: red;
      content: "*";
      position: absolute;
      margin-left: -15px;
    }
  </style>
</head>

<body>
  % include('base.tpl')
  <header>
  </header>
  <div class="container-fluid">

    % if jobtype:
    <h1 class="logo">Edit Jobtype "{{jobtype.name}}"</h1>
    <form class="p-3" method="post" action="/jobtype_edit/{{jobtype.id}}">

      <div class="form-group required">
        <b><label class='control-label'>Jobtype:</label></b>
        <input type="text" id="name" class="form-control" name="name" value="{{jobtype.name}}" required>
      </div>
      <input type="submit" class="btn btn-primary" value="Submit">
    </form>

    % else:

    <h1 class="logo">Add New Jobtype</h1>
    <form class="p-3" method="post" action="/jobtype_add">

      <div class="form-group required">
        <b><label class='control-label' for="fname">Jobtype:</label></b>
        <input type="text" id="name" class="form-control" name="name" required>
      </div>
      <input type="submit" class="btn btn-primary" value="Submit" id="confirm">

    </form>

    % end

  </div>
</body>

</html>