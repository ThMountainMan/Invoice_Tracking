<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
  <meta charset="utf-8">
  <title>Invoice Tracker</title>
  <style>
  </style>
</head>

<body>
  % include('base.tpl')
  <header>
    <div class="container">
      <h1 class="logo">Invoice Details for Invoice : {{input.invoice_id}}</h1>
      <table class=" table">
        <thead class="thead-light">
          <tr>
            <th>Invoide ID</th>
            <th>Invoide Date</th>
            <th>Customer Name</th>
            <th>Job Type</th>
            <th>Ammount</th>
            <th>Paydate</th>
            <th>Download</th>
        </thead>
        </tr>

        <tr>
          <td>{{input.invoice_id}}</td>
          <td>{{input.date}}</td>
          <td>{{input.customer.name}}</td>
          <td>{{input.jobtype.name}}</td>
          <td>{{input.invoice_ammount}} €</td>
          <td>{{input.paydate}}</td>
          <td>-</td>
        </tr>



    </div>
  </header>


</body>

</html>