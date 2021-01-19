<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
  <meta charset="utf-8">
  <title>Invoice Tracker</title>
  <style>
    form {
      max-width: 500px;
      display: block;
      margin: 1 auto;
    }
  </style>
</head>

<body>
  % include('base.tpl')

  <div class="container">

    % if expense:
    <form class="p-3" method="post" action="/expense_edit/{{expense.id}}">

      <h1 class="logo">Edit Expense</h1>

      <div class="form-group">
        <b><label for="expense_id">Expense ID:</label></b>
        <input type="text" id="expense_id" class="form-control" name="expense_id" value="{{expense.expense_id}}">
      </div>
      <div class="form-group">
        <b><label for="date">Date:</label></b>
        <input type="date" id="date" class="form-control" name="date" value="{{expense.date}}">
      </div>
      <div class="form-group">
        <b><label for="cost">Cost:</label></b>
        <input type="number" id="cost" class="form-control" name="cost" value="{{expense.cost}}">
      </div>

      <div class="form-group">
        <b><label for="comment">Comment:</label></b>
        <input type="text" id="comment" class="form-control" name="comment" value="{{expense.comment}}">
      </div>
      <input type="submit" class="btn btn-primary" value="Submit">
    </form>
    % else:
    <form class="p-3" method="post" action="/expense_add">
      <h1 class="logo">Add New Expense</h1>

      <div class="form-group">
        <b><label for="expense_id">Expense ID:</label></b>
        <input type="text" id="expense_id" class="form-control" name="expense_id" value="{{id}}">
      </div>
      <div class="form-group">
        <b><label for="date">Date:</label></b>
        <input type="date" id="date" class="form-control" name="date">
      </div>
      <div class="form-group">
        <b><label for="cost">Cost:</label></b>
        <input type="number" id="cost" class="form-control" name="cost">
      </div>

      <div class="form-group">
        <b><label for="comment">Comment:</label></b>
        <input type="text" id="comment" class="form-control" name="comment">
      </div>
      <input type="submit" class="btn btn-primary" value="Submit">
    </form>
    % end

  </div>
</body>

<script>
  function inputFocus(i) {
    if (i.value == i.defaultValue) {
      i.value = "";
      i.style.color = "#000";
    }
  }

  function inputBlur(i) {
    if (i.value == "") {
      i.value = i.defaultValue;
      i.style.color = "#888";
    }
  }
</script>

</html>