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
    <div class="container">

      <h1 class="logo">Edit / Add Invoices</h1>

      <form class="p-3" method="post" action="/invoice_add">
        <div class="form-group required">
          <b>
            <labe class='control-label'>Invoice ID:</label>
          </b>
          <input type="text" id="id" class="form-control" name="id" value={{id}} required>
        </div>

        <div class="form-group required">
          <b>
            <labe class='control-label'>Mwst.:</label>
          </b>
          <input type="number" id="mwst" class="form-control" name="mwst" min="0" max="20" value="16" required>
        </div>

        <div class="form-group required">
          <b>
            <labe class='control-label'>Invoice Date:</label>
          </b>
          <input type="date" id="date" class="form-control" name="date" required>
        </div>

        <div class="form-group required">
          <b>
            <labe class='control-label'>Customer:</label>
          </b>
          <select id="customer_id" class="form-control" name="customer_id" required>
            % for customer in customers:
            <option value={{customer.id}}>{{customer.name}}</option>
            % end
          </select>
        </div>

        <div class="form-group required">
          <b>
            <labe class='control-label'>Jobtype</label>
          </b>
          <select id="jobtype_id" class="form-control" name="jobtype_id" required>
            % for jobtype in jobtypes:
            <option value={{jobtype.id}}>{{jobtype.name}}</option>
            % end
          </select>
        </div>

        <div class="form-group required">
          <b>
            <labe class='control-label'>Agency:</label>
          </b>
          <select id="agency_id" class="form-control" name="agency_id" required>
            % for agency in agencys:
            <option value={{jobtype.id}}>{{agency.name}}</option>
            % end
          </select>
        </div>



        <div class="form-group required invoice" id="otherFieldGroupDiv" name=Test123>
          <b>
            <label for="agency">Invoice Details:</label>
          </b>
          <div class="row">
            <div class="col-6">
              <labe class='control-label'>Item Count:</label>
                <input type="number" class="form-control w-100" name=ammount1 id="ammount1" required>
            </div>
            <div class="col-6">
              <labe class='control-label'>Price:</label>
                <input type="number" class="form-control w-100" name=price1 id=="price1" required>
            </div>
            <div class="col-6">
              <labe class='control-label'>Description:</label>
                <textarea class="form-control w-100" id="comment1" name=comment1 rows="1" required></textarea>
            </div>
          </div>
        </div>

        <div id="newRow">
          <button id="addRow" type="button" class="btn btn-info">Additional Item</button>
        </div><br>

        <input type="submit" class="btn btn-primary" value="Submit">
      </form>
    </div>
  </header>
</body>

<script>
  // add row
  $("#addRow").click(function() {
    var html = '';

    html += '<div id="inputFormRow">' +
      '<div class="form-group required invoice" id="otherFieldGroupDiv" name=Test123>' +
      '<b><labe class='
    control - label ' for="agency">Invoice Details:</label></b>' +
      '<div class="row">' +
      '<div class="col-6">' +
      '<labe class='
    control - label ' for="otherField1">Amount:</label>' +
      '<input type="text" class="form-control w-100" name=amount[] id="otherField1">' +
      '</div>' +
      '<div class="col-6">' +
      '<labe class='
    control - label ' for="otherField2">Price:</label>' +
      '<input type="text" class="form-control w-100" name=price[]="otherField2">' +
      '</div>' +
      '<div class="col-6">' +
      '<labe class='
    control - label ' for="comments">Description:</label>' +
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