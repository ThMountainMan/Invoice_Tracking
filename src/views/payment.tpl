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
    <h1 class="logo">Payment Details Data</h1>
    <br><a href="/payment_add" class="btn btn-primary"> Add New Payment Method </a><br><br>
    <table class=" table">
      <thead class="thead-light">
        <tr>
          <th>Label</th>
          <th>Bank Details</th>
          <th>EDIT</th>
        </tr>
      </thead>
      % for data in input:
      <tr>
        <td><strong>{{data.label}}</strong></td>
        <td>
          {{data.name}}<br>
          {{data.bank}}<br>
          {{data.IBAN}}<br>
          {{data.BIC}}<br>
        </td>

        <td>
          <button onclick="location.href = '/payment_edit/{{data.id}}';" type="button" class="btn btn-warning btn-sm">EDIT</button>
          <button onclick="location.href = '/payment_delete/{{data.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button>
        </td>
      </tr>
      % end


  </div>



</body>

</html>