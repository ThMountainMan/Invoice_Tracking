<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="utf-8">
  <title>Invoice Tracker</title>
  <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }

    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #dddddd;
    }
</style>
</head>
<body>
  % include('base.tpl')
   <header>
     <div class="container">
       <h1 class="logo">Invoice Details for Invoice : {{input.invoice_id}}</h1>
       <table>
          <tr>
            <th>Invoide ID</th>
            <th>Invoide Date</th>
            <th>Customer Name</th>
            <th>Job Type</th>
            <th>Ammount</th>
            <th>Paydate</th>

          </tr>

          <tr>
            <td>{{input.invoice_id}}</td>
            <td>{{input.date}}</td>
            <td>{{input.customer.name}}</td>
            <td>{{input.jobtype.name}}</td>
            <td>{{input.invoice_ammount}} €</td>
            <td>{{input.paydate}}</td>
          </tr>



     </div>
   </header>


</body>
</html>
