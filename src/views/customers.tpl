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
  <header>
    <div class="container-fluid">
      <h1 class="logo">Customers</h1>
      <br><a href="/customer_add" class="btn btn-primary"> Create New Customer </a><br><br>
      <table class="table">
        <thead class="thead-light">
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Contact Person</th>
            <th>Contact Details</th>
            <th>Adress</th>
            <th>EDIT</th>
          </tr>
        </thead>
        % for customer in input:
        <tr>
          <td>{{customer.id}}</td>
          <td>{{customer.name}}</td>
          <td>{{customer.contact}}</td>
          <td>{{customer.email}}<br>
            {{customer.phone}}
          </td>
          <td>{{customer.street}} <br>
            {{customer.postcode}} <br>
            {{customer.city}} <br>
            {{customer.country}} <br>
          </td>
          <td>
            <button onclick="location.href = '/customer_edit/{{customer.id}}';" type="button" class="btn btn-warning btn-sm">EDIT</button>
            <button onclick="location.href = '/customer_delete/{{customer.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button>
          </td>
        </tr>
        % end


    </div>
  </header>


</body>

</html>