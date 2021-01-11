<!DOCTYPE html>
<html lang="en" dir="ltr">

<link rel="stylesheet" type="text/css" href="/static/style.css">
<script src="/static/jquery-3.2.1.slim.min.js"></script>
<script src="/static/bootstrap.min.js"></script>


<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>

<head>
  <meta charset="utf-8">
  <title>Invoice Tracker</title>
  <style>
    form {
      max-width: 500px;
      display: block;
      margin: 1 auto;
    }

    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }

    td,
    th {
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

      <h1 class="logo">Edit / Add Invoices</h1>

      <form class="p-3" action="/invoices_add">
        <div class="form-group">
          <b><label for="fname">Invoice ID:</label></b>
          <input type="text" id="invoice_id" class="form-control" name="invoice_id" value="John">
        </div>

        <div class="form-group">
          <b><label for="date">Invoice Date:</label></b>
          <input type="date" id="invoice_date" class="form-control" name="invoice_date">
        </div>

        <div class="form-group">
          <b><label for="customer">Customer:</label></b>
          <select id="customer" class="form-control" name="customer_id">
            % for customer in customers:
            <option value={{customer.id}}>{{customer.name}}</option>
            % end
            <option value=create_new_customer> --CREATE NEW CUSTOMER -- </option>
          </select>
        </div>

        <div class="form-group">
          <b><label for="jobtype">Jobtype</label></b>
          <select id="jobtype" class="form-control" name="jobtype_id">
            % for jobtype in jobtypes:
            <option value={{jobtype.id}}>{{jobtype.name}}</option>
            % end
          </select>
        </div>

        <div class="form-group">
          <b><label for="agency">Agency:</label></b>
          <select id="agency" class="form-control" name="agencys_id">
            % for agency in agencys:
            <option value={{jobtype.id}}>{{agency.name}}</option>
            % end
          </select>
        </div>

        <div id="newRow">
          <button id="addRow" type="button" class="btn btn-info">Additional Item</button>
        </div>

        <div class="form-group" id="otherFieldGroupDiv" name=Test123>
          <b><label for="agency">Invoice Details:</label></b>
          <div class="row">
            <div class="col-6">
              <label for="otherField1">Amount:</label>
              <input type="text" class="form-control w-100" name=amount1 id="otherField1">
            </div>
            <div class="col-6">
              <label for="otherField2">Price:</label>
              <input type="text" class="form-control w-100" name=price1="otherField2">
            </div>
            <div class="col-6">
              <label for="comments">Description:</label>
              <textarea class="form-control w-100" id="comments" name=comment1 rows="1"></textarea>
            </div>
          </div>
        </div>

        <input type="submit" class="btn btn-primary" value="Submit">
      </form>

      <p>On Submit the new Invoice will be created ....</p>


    </div>
  </header>
</body>

<script>
  // add row
  $("#addRow").click(function() {
    var html = '';

    html += '<div id="inputFormRow">' +
      '<div class="form-group" id="otherFieldGroupDiv" name=Test123>' +
      '<b><label for="agency">Invoice Details:</label></b>' +
      '<div class="row">' +
      '<div class="col-6">' +
      '<label for="otherField1">Amount:</label>' +
      '<input type="text" class="form-control w-100" name=amount[] id="otherField1">' +
      '</div>' +
      '<div class="col-6">' +
      '<label for="otherField2">Price:</label>' +
      '<input type="text" class="form-control w-100" name=price[]="otherField2">' +
      '</div>' +
      '<div class="col-6">' +
      '<label for="comments">Description:</label>' +
      '<textarea class="form-control w-100" id="comments" name=comment[] rows="1"></textarea>' +
      '</div>' +
      '<button id="removeRow" type="button" class="btn btn-danger">Remove</button>' +
      '</div>' +
      '</div>' +
      '</div>'

    $('#newRow').append(html);
  });

  // remove row
  $(document).on('click', '#removeRow', function() {
    $(this).closest('#inputFormRow').remove();
  });
</script>

</html>