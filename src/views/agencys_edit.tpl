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

  <div class="container-fluid">

    % if agency:
    <h1 class="logo">Edit agency "{{agency.name}}"</h1>
    <form class="p-3" method="post" action="/agency_edit/{{agency.id}}">

      <div class="form-group required">
        <b><label class='control-label' for="fname">Name:</label></b>
        <input type="text" id="name" class="form-control" name="name" value="{{agency.name}}" required>
      </div>

      <div class="form-group required">
        <b><label class='control-label' for="date">Percentage:</label></b>
        <input type="number" id="percentage" class="form-control" name="percentage" value="{{agency.percentage}}" required>
      </div>

      <input type="submit" class="btn btn-primary" value="Submit">
    </form>


    % else:
    <h1 class="logo">Add New agency</h1>
    <form class="p-3" method="post" action="/agency_add">

      <div class="form-group required">
        <b><label class='control-label' for="fname">Name:</label></b>
        <input type="text" id="name" class="form-control" name="name" required>
      </div>

      <div class="form-group required">
        <b><label class='control-label' for="date">Percentage:</label></b>
        <input type="number" id="percentage" class="form-control" name="percentage" min="0" max="20" value="16" required>
      </div>

      <input type="submit" class="btn btn-primary" value="Submit">

    </form>
    % end

  </div>
</body>

</html>