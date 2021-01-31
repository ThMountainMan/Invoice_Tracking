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

    <h1 class="logo">Edit / Add Invoices</h1>

    <form class="p-3" method="post" action="/invoice_add">


      <div class="form-group required">
        <b><label class='control-label'>Invoice ID:</label></b>
        <input readonly type="text" id="id" class="form-control" name="id" value={{id}} required>
      </div>

      <div class="form-group required">
        <b><label class='control-label'>Personal / Bank Details:</label></b>
        <select id="personal_id" class="form-control" name="personal_id" required>
          % for person in personas:
          <option value={{person.id}}>{{person.label.upper()}}</option>
          % end
        </select>
      </div>

      <div class="form-group required">
        <b><label class='control-label'>Invoice Date:</label></b>
        <input type="date" id="date" class="form-control" name="date" required>
      </div>

      <div class="form-group required">
        <b><label class='control-label'>Customer:</label></b>
        <select id="customer_id" class="form-control" name="customer_id" required>
          % for customer in customers:
          <option value={{customer.id}}>{{customer.name}}</option>
          % end
        </select>
      </div>

      <div class="form-group required">
        <b><label class='control-label'>Jobtype</label></b>
        <select id="jobtype_id" class="form-control" name="jobtype_id" required>
          % for jobtype in jobtypes:
          <option value={{jobtype.id}}>{{jobtype.name}}</option>
          % end
        </select>
      </div>

      <div class="form-group required">
        <b><label class='control-label'>Agency:</label></b>
        <select id="agency_id" class="form-control" name="agency_id" required>
          <option value=None>--</option>
          % for agency in agencys:
          <option value={{jobtype.id}}>{{agency.name}}</option>
          % end
        </select>
      </div>

      <div class="form-group required">
        <b><label class='control-label'>Mwst.:</label></b>
        <div class="input-group-prepend">
          <input type="number" id="mwst" class="form-control" name="mwst" min="0" max="20" value="19" required>
          <span class="input-group-text" id="basic-addon1">%</span>
        </div>
      </div>

      <div class="form-group required invoice" id="otherFieldGroupDiv" name=Test123>
        <h3>Invoice Details:</h3>
        <small id="passwordHelpBlock" class="form-text text-muted">
          Please Fill the Boxes with details about the Invoic. For example: <br>
          Item Count : 1 <br>
          Price : 245 <br>
          Description: I Have done this and that for the company
        </small>
        <br>
        <div id="itemlist1" class="itemlist">
          <div class="row">
            <div class="col-6">
              <b><label class='control-label'>Item Count:</label></b>
              <input type="number" class="form-control w-100" name="ammount" onkeypress="return event.charCode >= 48" min="1" required>
            </div>
            <div class="col-6">
              <b><label class='control-label'>Price:</label></b>
              <div class="input-group-prepend">
                <input type="number" class="form-control w-100" name="price" required>
                <span class="input-group-text" id="basic-addon1">€</span>
              </div>
            </div>

            <div class="col-12">
              <b><label class='control-label'>Description:</label></b>
              <textarea class="form-control w-100" name="comment" rows=" 3" required></textarea>
            </div>
          </div>
          <br>
        </div>
        <div id="moreitemlist" class="moreitemlist"></div>
      </div>

      <div id="newRow">
        <button id="additem" type="button" class="btn btn-info">Additional Item</button>
        <button id="removeitem" type="button" class="btn btn-danger">Remove</button>
      </div><br>

      <input type="submit" class="btn btn-primary" value="Submit">
    </form>
  </div>

</body>


<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>

<script>
  $(document).ready(function() {
    $('#additem').click(function() {
      var num = $('.itemlist').length;
      var newNum = new Number(num + 1);

      var newSection = $('#itemlist' + num).clone().attr('id', 'itemlist' + newNum);

      // Change the Names of the input fields
      //newSection.children(':first').children(':first').attr('id', 'name' + newNum).attr('name', 'name' + newNum);
      //newSection.children(':nth-child(2)').children(':first').attr('id', 'nameTwo' + newNum).attr('name', 'nameTwo' + newNum);
      //newSection.children(':nth-child(3)').children(':first').attr('id', 'nameTwo' + newNum).attr('name', 'nameTwo' + newNum);

      // Add the clone to the section
      $('.itemlist').last().append(newSection)
      // Enable the Disable button
      $('#removeitem').attr('disabled', '');

      // If there are more then X items, do not allow the creation of more
      if (newNum == 5)
        $('#additem').attr('disabled', 'disabled');
    });

    $('#removeitem').click(function() {
      var num = $('.itemlist').length; // how many "duplicatable" input fields we currently have
      $('#itemlist' + num).remove(); // remove the last element

      // enable the "add" button
      $('#additem').attr('disabled', '');

      // if only one element remains, disable the "remove" button
      if (num - 1 == 1)
        $('#removeitem').attr('disabled', 'disabled');
    });

    $('#removeitem').attr('disabled', 'disabled');
  });
</script>

</html>