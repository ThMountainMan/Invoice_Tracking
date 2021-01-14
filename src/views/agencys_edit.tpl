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
  </style>
</head>

<body>
  % include('base.tpl')
  <header>
    <div class="container">
      % if agency:
      <h1 class="logo">Edit agency "{{agency.name}}"</h1>
      <form class="p-3" method="post" action="/agency_edit/{{agency.id}}">
        % else:
        <h1 class="logo">Add New agency</h1>
        <form class="p-3" method="post" action="/agency_add">
          % end

          <div class="form-group">
            <b><label for="fname">Name:</label></b>
            % if agency:
            <input type="text" id="name" class="form-control" name="name" value="{{agency.name}}">
            % else:
            <input type="text" id="name" class="form-control" name="name" style="color:#888;" value="Agency Name" onfocus="inputFocus(this)" onblur="inputBlur(this)">
            % end
          </div>

          <div class="form-group">
            <b><label for="date">Percentage:</label></b>
            % if agency:
            <input type="number" id="percentage" class="form-control" name="percentage" value="{{agency.percentage}}">
            % else:
            <input type="number" id="percentage" class="form-control" name="percentage" min="0" max="20" value="16">
            %end
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