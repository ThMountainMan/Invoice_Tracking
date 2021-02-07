<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
  <meta charset="utf-8">
  <title>CCC Tracker</title>
  <style>

  </style>

  % include('base.tpl')
</head>

<body>

  <header>
    <div class="container-fluid">
      <h1 class="logo">Agencys</h1>
      <br><a href="/agency_add" class="btn btn-primary"> Create New Agency </a><br><br>
      <table class=" table">
        <thead class="thead-light">
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Percentage</th>
            <th>EDIT</th>

          </tr>
        </thead>
        % for agency in input:
        <tr>
          <td>{{agency.id}}</td>
          <td>{{agency.name}}</td>
          <td>{{agency.percentage}}</td>
          <td>
            <button onclick="location.href = '/agency_edit/{{agency.id}}';" type="button" class="btn btn-warning btn-sm">EDIT</button>
            <button onclick="location.href = '/agency_delete/{{agency.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button>
          </td>
        </tr>
        % end


    </div>
  </header>


</body>

</html>