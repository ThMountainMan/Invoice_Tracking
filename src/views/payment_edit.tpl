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
  <header>
    <div class="container-fluid">

      % if data:

      <h1 class="logo">Edit Payment Details "{{data.label}}"</h1>
      <form class="p-3" method="post" action="/payment_edit/{{data.id}}">

        <div class="form-group required">
          <b><label class='control-label'>LABEL:</label></b>
          <input type="text" id="label" class="form-control" name="label" value="{{data.label}}" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Name:</label></b>
          <input type="text" id="name" class="form-control" name="name" value="{{data.name}}" required>
        </div>

        <div class="form-group">
          <b><label class='control-label'>Bank:</label></b>
          <input type="text" id="bank" class="form-control" name="bank" value="{{data.bank}}" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>IBAN:</label></b>
          <input type="text" id="IBAN" class="form-control" name="IBAN" value="{{data.IBAN}}" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>BIC:</label></b>
          <input type="text" id="BIC" class="form-control" name="BIC" value="{{data.BIC}}" required>
        </div>


        <input type="submit" class="btn btn-primary" value="Submit">

      </form>

      % else:
      <h1 class="logo">Payment Details</h1>
      <form class="p-3" method="post" action="/payment_add">

        <div class="form-group required">
          <b><label class='control-label'>LABEL:</label></b>
          <input type="text" id="label" class="form-control" name="label" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Name:</label></b>
          <input type="text" id="name" class="form-control" name="name" required>
        </div>

        <div class="form-group">
          <b><label class='control-label'>Bank:</label></b>
          <input type="text" id="bank" class="form-control" name="bank" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>IBAN:</label></b>
          <input type="text" id="IBAN" class="form-control" name="IBAN" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>BIC:</label></b>
          <input type="text" id="BIC" class="form-control" name="BIC" required>
        </div>

        <input type="submit" class="btn btn-primary" value="Submit">

      </form>

      %end
    </div>
  </header>
</body>


</html>