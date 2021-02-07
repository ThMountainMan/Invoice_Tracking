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
      <h1 class="logo">Expenses</h1>
      <br><a href="/expense_add" class="btn btn-primary"> Add New Expense </a><br><br>
      <table class="table">
        <thead class="thead-light">
          <tr>
            <th>Expense ID</th>
            <th>Date</th>
            <th>Cost</th>
            <th>Comment</th>
            <th>EDIT</th>
          </tr>
        </thead>
        % for expense in input:
        <tr>
          <td>{{expense.expense_id}}</td>
          <td>{{expense.date}}</td>
          <td>{{expense.cost}} €</td>
          <td>{{expense.comment}}</td>
          <td>
            <button onclick="location.href = '/expense_edit/{{expense.id}}';" type="button" class="btn btn-warning btn-sm">EDIT</button>
            <button onclick="location.href = '/expense_delete/{{expense.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button>
          </td>
        </tr>
        % end


    </div>
  </header>


</body>

</html>