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

    .form-group.required .control-label:before {
      color: red;
      content: "*";
      position: absolute;
      margin-left: -15px;
    }
  </style>
</head>

<body>
  % include('base.tpl')

  <div class="container-fluid">

    % if expense:
    <form class="p-3" method="post" action="/expense_edit/{{expense.id}}">

      <h1 class="logo">Edit Expense</h1>

      <div class="form-group required">
        <b><label class='control-label'>Expense ID:</label></b>
        <input type="text" id="expense_id" class="form-control" name="expense_id" value="{{expense.expense_id}}" readonly>
      </div>
      <div class="form-group required">
        <b><label class='control-label'>Date:</label></b>
        <input type="date" id="date" class="form-control" name="date" value="{{expense.date}}" required>
      </div>
      <div class="form-group required">
        <b><label class='control-label'>Cost:</label></b>
        <input type="number" step=".01" id="cost" class="form-control" name="cost" value="{{expense.cost}}" required>
      </div>

      <div class="form-group required">
        <b><label class='control-label'>Comment:</label></b>
        <input type="text" id="comment" class="form-control" name="comment" value="{{expense.comment}}" required>
      </div>
      <input type="submit" class="btn btn-primary" value="Submit">
    </form>
    % else:
    <form class="p-3" method="post" action="/expense_add">
      <h1 class="logo">Add New Expense</h1>

      <div class="form-group required">
        <b><label class='control-label'>Expense ID:</label></b>
        <input type="text" id="expense_id" class="form-control" name="expense_id" value="{{new_id}}" readonly>
      </div>
      <div class="form-group required">
        <b>
          <label class='control-label'>Date:</label>
        </b>
        <input type="date" id="date" class="form-control" name="date" required>
      </div>
      <div class="form-group required">
        <b><label class='control-label'>Cost:</label></b>
        <input type="number" step=".01" id="cost" class="form-control" name="cost" required>
      </div>

      <div class="form-group required">
        <b><label class='control-label'>Comment:</label></b>
        <input type="text" id="comment" class="form-control" name="comment" required>
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