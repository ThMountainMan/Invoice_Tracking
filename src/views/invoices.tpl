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
      <h1 class="logo">All available invoices</h1>
      <br><a href="/invoice_add" class="btn btn-primary"> Create New Invoice </a><br><br>
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
        % for invoice in input:
        <tr>
          <td><a href="/invoices/{{invoice.id}}">{{invoice.invoice_id}}</a></td>
          <td>{{invoice.date}}</td>
          <td>{{invoice.customer.name}}</td>
          <td>{{invoice.jobtype.name}}</td>
          <td>{{invoice.invoice_ammount}} €</td>
          <td>{{invoice.paydate}}</td>
          <td>
            <button class="btn btn-primary btn-sm"><i class="fa fa-download"></i></button>
            <button onclick="location.href = '/invoice_delete/{{invoice.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button>
          </td>
        </tr>
        % end


    </div>
  </header>


</body>

</html>