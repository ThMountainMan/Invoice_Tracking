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

    .form-group.required .control-label:after {
      content: "*";
      color: red;
    }
  </style>
</head>

<body>
  % include('base.tpl')
  <header>
    <div class="container">

      % if customer:
      <h1 class="logo">Edit Customer "{{customer.name}}"</h1>
      <form class="p-3" method="post" action="/customer_edit/{{customer.id}}">
        % else:
        <h1 class="logo">Add New Customer</h1>
        <form class="p-3" method="post" action="/customer_add">
          % end

          <div class="form-group">
            <b><label class='control-label' for="fname">Customer Name:</label></b>
            % if customer:
            <input type="text" id="name" class="form-control" name="name" value="{{customer.name}}">
            % else:
            <input type="text" id="name" class="form-control" name="name" style="color:#888;" value="Name" onfocus="inputFocus(this)" onblur="inputBlur(this)">
            % end
          </div>

          <div class="form-group">
            <b><label for="fname">Customer Contact:</label></b>
            % if customer:
            <input type="text" id="contact" class="form-control" name="contact" value="{{customer.contact}}">
            % else:
            <input type="text" id="contact" class="form-control" name="contact" style="color:#888;" value="Contact Person" onfocus="inputFocus(this)" onblur="inputBlur(this)">
            % end
          </div>

          <div class="form-group">
            <b><label for="fname">E-Mail:</label></b>
            % if customer:
            <input type="text" id="email" class="form-control" name="email" value=" -- ">
            % else:
            <input type="text" id="email" class="form-control" name="email" style="color:#888;" value="E-Mail" onfocus="inputFocus(this)" onblur="inputBlur(this)">
            % end
          </div>

          <div class="form-group">
            <b><label for="fname">Phone:</label></b>
            % if customer:
            <input type="text" id="email" class="form-control" name="email" value=" -- ">
            % else:
            <input type="text" id="email" class="form-control" name="email" style="color:#888;" value="E-Mail" onfocus="inputFocus(this)" onblur="inputBlur(this)">
            % end
          </div>

          <div class="form-group">
            <b><label for="fname">Street:</label></b>
            % if customer:
            <input type="text" id="street" class="form-control" name="street" value="{{customer.street}}">
            % else:
            <input type=" text" id="street" class="form-control" name="street" style="color:#888;" value="Street" onfocus="inputFocus(this)" onblur="inputBlur(this)">
            % end
          </div>

          <div class="form-group">
            <div class="row">
              <div class="col-6">
                <b><label for="fname">Postcode:</label></b>
                % if customer:
                <input type="text" id="postcode" class="form-control" name="postcode" value={{customer.postcode}}>
                % else:
                <input type="text" id="postcode" class="form-control" name="postcode" style="color:#888;" value="Postcode" onfocus="inputFocus(this)" onblur="inputBlur(this)">
                % end
              </div>
              <div class="col-6">
                <b><label for="fname">City:</label></b>
                % if customer:
                <input type="text" id="city" class="form-control" name="city" value="{{customer.city}}">
                % else:
                <input type="text" id="city" class="form-control" name="city" style="color:#888;" value="City" onfocus="inputFocus(this)" onblur="inputBlur(this)">
                % end
              </div>
            </div>
          </div>


          <div class="form-group">
            <b><label for="fname">Country:</label></b>
            % if customer:
            <input type="text" id="country" class="form-control" name="country" value="{{customer.country}}">
            % else:
            <input type="text" id="country" class="form-control" name="country" style="color:#888;" value="Country" onfocus="inputFocus(this)" onblur="inputBlur(this)">
            % end
          </div>

          <input type="submit" class="btn btn-primary" value="Submit">

        </form>
    </div>
  </header>
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