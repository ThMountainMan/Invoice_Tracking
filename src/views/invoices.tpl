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

    .button {
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

.button1 {background-color: #4CAF50;} /* Green */
.button2 {background-color: #008CBA;} /* Blue */

</style>
</head>
<body>
  % include('base.tpl')
   <header>
     <div class="container">
       <h1 class="logo">All available invoices</h1>
       <br><a href="/invoices_add" class="button button1"> Create New Invoice </a><br><br><br>
       <table>
          <tr>
            <th>Invoide ID</th>
            <th>Invoide Date</th>
            <th>Customer Name</th>
            <th>Job Type</th>
            <th>Ammount</th>
            <th>Paydate</th>

          </tr>
          % for invoice in input:
          <tr>
            <td><a href="/invoices/{{invoice.id}}">{{invoice.invoice_id}}</a></td>
            <td>{{invoice.date}}</td>
            <td>{{invoice.customer.name}}</td>
            <td>{{invoice.jobtype.name}}</td>
            <td>{{invoice.invoice_ammount}} €</td>
            <td>{{invoice.paydate}}</td>
          </tr>
          % end


     </div>
   </header>


</body>
</html>
