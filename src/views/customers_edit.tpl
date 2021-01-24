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

    % if customer:
    <h1 class="logo">Edit Customer "{{customer.name}}"</h1>
    <form class="p-3" method="post" action="/customer_edit/{{customer.id}}">

      <div class="form-group required">
        <b><label class='control-label' for="fname">Customer Name:</label></b>
        <input type="text" id="name" class="form-control" name="name" value="{{customer.name}}" required>
      </div>

      <div class="form-group">
        <b><label for="fname">Customer Contact:</label></b>
        <input type="text" id="contact" class="form-control" name="contact" value="{{customer.contact}}">
      </div>

      <div class="form-group">
        <b><label class='control-label' for="fname">E-Mail:</label></b>
        <input type="email" id="email" class="form-control" name="email" value="{{customer.email}}">
      </div>

      <div class="form-group">
        <b><label class='control-label' for="fname">Phone:</label></b>
        <input type="text" id="phone" class="form-control" name="phone" value="{{customer.phone}}">
      </div>

      <div class="form-group required">
        <b><label class='control-label' for="fname">Street:</label></b>
        <input type="text" id="street" class="form-control" name="street" value="{{customer.street}}" required>
      </div>

      <div class="form-group required">
        <div class="row">
          <div class="col-6">
            <b><label class='control-label' for="fname">Postcode:</label></b>
            <input type="text" id="postcode" class="form-control" name="postcode" value={{customer.postcode}} required>
          </div>
          <div class="col-6">
            <b><label class='control-label' for="fname">City:</label></b>
            <input type="text" id="city" class="form-control" name="city" value="{{customer.city}}" required>
          </div>
        </div>
      </div>

      <div class="form-group">
        <b><label class='control-label' for="fname">Country:</label></b>
        <input type="text" id="country" class="form-control" name="country" value="{{customer.country}}">
      </div>

      <input type="submit" class="btn btn-primary" value="Submit">

    </form>

    % else:
    <h1 class="logo">Add New Customer</h1>
    <form class="p-3" method="post" action="/customer_add">

      <div class="form-group required">
        <b><label class='control-label' for="fname">Customer Name:</label></b>
        <input type="text" id="name" class="form-control" name="name" required>
      </div>

      <div class="form-group">
        <b><label class='control-label' for="fname">Customer Contact:</label></b>
        <input type="text" id="contact" class="form-control" name="contact">
      </div>

      <div class="form-group">
        <b><label class='control-label' for="fname">E-Mail:</label></b>
        <input type="text" id="email" class="form-control" name="email">
      </div>

      <div class="form-group">
        <b><label class='control-label' for="fname">Phone:</label></b>
        <input type="text" id="phone" class="form-control" name="phone">
      </div>

      <div class="form-group required">
        <b><label class='control-label' for="fname">Street:</label></b>
        <input type=" text" id="street" class="form-control" name="street" required>
      </div>

      <div class="form-group required">
        <div class="row">
          <div class="col-6">
            <b><label class='control-label' for="fname">Postcode:</label></b>
            <input type="text" id="postcode" class="form-control" name="postcode" required>
          </div>
          <div class="col-6">
            <b><label class='control-label' for="fname">City:</label></b>
            <input type="text" id="city" class="form-control" name="city" required>
          </div>
        </div>
      </div>

      <div class="form-group">
        <b><label class='control-label' for="fname">Country:</label></b>
        <input type="text" id="country" class="form-control" name="country">
      </div>

      <input type="submit" class="btn btn-primary" value="Submit">

    </form>

    % end

  </div>
</body>

</html>