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

      <h1 class="logo">Edit Personal Data "{{data.label}}"</h1>
      <form class="p-3" method="post" action="/personal_edit/{{data.id}}">

        <div class="form-group required">
          <b><label class='control-label'>LABEL:</label></b>
          <input type="text" id="label" class="form-control" name="label" value="{{data.label}}" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Name:</label></b>
          <input type="text" id="name" class="form-control" name="name" value="{{data.name}}" required>
        </div>

        <div class="form-group">
          <b><label class='control-label'>Company Name:</label></b>
          <input type="text" id="company_name" class="form-control" name="company_name" value="{{data.name_company}}">
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Tax Number:</label></b>
          <input type="text" id="taxnumber" class="form-control" name="taxnumber" value="{{data.taxnumber}}" required>
        </div>

        <div class="form-group required">
          <b>
            <labe class='control-label'>Payment Details:</label>
          </b>
          <select id="payment_details" class="form-control" name="payment_details" required>
            % for details in payment:
            <option value={{details.id}}>{{details.label}}</option>
            % end
          </select>
        </div>


        <div class="form-group required">
          <b><label class='control-label'>E-Mail:</label></b>
          <input type="email" id="mail" class="form-control" name="mail" value="{{data.mail}}" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Phone:</label></b>
          <input type="text" id="phone" class="form-control" name="phone" value="{{data.phone}}" required>
        </div>

        <div class="form-group required">
          <b>
            <labe class='control-label' l>Street:</label>
          </b>
          <input type="text" id="street" class="form-control" name="street" value="{{data.street}}" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Postcode:</label></b>
          <input type="text" id="postcode" class="form-control" name="postcode" value="{{data.postcode}}" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>City:</label></b>
          <input type="text" id="city" class="form-control" name="city" value="{{data.city}}" required>
        </div>


        <input type="submit" class="btn btn-primary" value="Submit">

      </form>

      % else:
      <h1 class="logo">Add Personal Data</h1>
      <form class="p-3" method="post" action="/personal_add">

        <div class="form-group required">
          <b><label class='control-label'>LABEL:</label></b>
          <input type="text" id="label" class="form-control" name="label" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Name:</label></b>
          <input type="text" id="name" class="form-control" name="name" required>
        </div>

        <div class="form-group">
          <b><label class='control-label'>Company Name:</label></b>
          <input type="text" id="company_name" class="form-control" name="company_name">
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Tax Number:</label></b>
          <input type="text" id="taxnumber" class="form-control" name="taxnumber" required>
        </div>

        <div class="form-group required">
          <b>
            <labe class='control-label'>Payment Details:</label>
          </b>
          <select id="payment_details" class="form-control" name="payment_details" required>
            % for details in payment:
            <option value={{details.id}}>{{details.label}}</option>
            % end
          </select>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>E-Mail:</label></b>
          <input type="text" id="mail" class="form-control" name="mail" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Phone:</label></b>
          <input type="text" id="phone" class="form-control" name="phone" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Street:</label></b>
          <input type="text" id="street" class="form-control" name="street" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>Postcode:</label></b>
          <input type="text" id="postcode" class="form-control" name="postcode" required>
        </div>

        <div class="form-group required">
          <b><label class='control-label'>City:</label></b>
          <input type="text" id="city" class="form-control" name="city" required>
        </div>

        <input type="submit" class="btn btn-primary" value="Submit">

      </form>

      %end
    </div>
  </header>
</body>


</html>