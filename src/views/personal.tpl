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

  <div class="container">
    <h1 class="logo">Personal Data</h1>
    <br><a href="/personal_add" class="btn btn-primary"> Add New Company / Personal Data </a><br><br>
    <table class=" table">
      <thead class="thead-light">
        <tr>
          <th>LABEL</th>
          <th>Name</th>
          <th>Contact Details</th>
          <th>Address</th>
          <th>Payment Details</th>
          <th>EDIT</th>
        </tr>
      </thead>
      % for data in input:
      <tr>
        <td><strong>{{data.label}}</strong></td>
        <td>{{data.name}}</td>
        <td>
          {{data.mail}}<br>
          {{data.phone}}
        </td>
        <td>
          {{data.street}}<br>
          {{data.postcode}}<br>
          {{data.city}}
        </td>
        <td>
          {{data.payment_datails.name}}<br>
          {{data.payment_datails.bank}}<br>
          {{data.payment_datails.IBAN}}<br>
          {{data.payment_datails.BIC}}<br>
        </td>
        <td>
          <button onclick="location.href = '/personal_edit/{{data.id}}';" type="button" class="btn btn-warning btn-sm">EDIT</button>
          <button onclick="location.href = '/personal_delete/{{data.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button>
        </td>
      </tr>
      % end


  </div>



</body>

</html>