<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
  <meta charset="utf-8">
  <title>CCC Tracker</title>
  <style>

  </style>
</head>

<body>
  % include('base.tpl')
  <div class="container-fluid">
    <h1 class="logo">Jobtypes</h1>
    <br><a href="/jobtype_add" class="btn btn-primary"> Create New Jobtype </a><br><br>
    <table class=" table">
      <thead class="thead-light">
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>EDIT</th>
        </tr>
      </thead>
      % for jobtype in input:
      <tr>
        <td>{{jobtype.id}}</td>
        <td>{{jobtype.name}}</td>
        <td>
          <button onclick="location.href = '/jobtype_edit/{{jobtype.id}}';" type="button" class="btn btn-warning btn-sm">EDIT</button>
          <button onclick="location.href = '/jobtype_delete/{{jobtype.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button>

        </td>
      </tr>
      % end


  </div>
</body>

</html>