% setdefault('title', 'Personal Details')
%include("base.tpl")
<div class="container-fluid">
  <div class="panel panel-default">
    <div class="panel-heading">
      <h1 class="panel-title">
        {{title}}
      </h1>
    </div>
    <div class="panel-body">
      <div class="clearfix">
        <button class="btn btn-primary" id="addRow">Add Row</button>
        <button type="button" class="btn btn-primary"
          style="margin-right:20px;">Reload</button>
      </div>
      <br />

      <table class="table table-hover" id="tableedit">
        <thead class="thead-light">
          <tr>
            <td style="display:none;"></td>
            <th>LABEL</th>
            <th>Name</th>
            <th>E-Mail</th>
            <th>Phone</th>
            <th>Street</th>
            <th>Postcode</th>
            <th>City</th>
            <th>Tax#</th>
            <th>Payment ID</th>
            <th>Payment Details</th>
          </tr>
        </thead>
        <tbody>
          <tr class="tableedit-template" style="display: none;">
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
          </tr>
            % for data in input:
            <tr>
              <td style="display:none;">{{data.id}}</td>
              <td><strong>{{data.label}}</strong></td>
              <td>{{data.name}}</td>
              <td>{{data.mail}}</td>
              <td>{{data.phone}}</td>
              <td>{{data.street}}</td>
              <td>{{data.postcode}}</td>
              <td>{{data.city}}</td>
              <td>{{data.taxnumber}}</td>
              <td>{{data.payment_details.label}}</td>
              <td>
                {{data.payment_details.name}}<br>
                {{data.payment_details.bank}}<br>
                {{data.payment_details.IBAN}}<br>
                {{data.payment_details.BIC}}<br>
              </td>
          </tr>
          % end
        </tbody>
      </table>

    </div> <!-- /.panel-body -->
  </div> <!-- /.panel -->
</div> <!-- row -->



<script type="text/javascript">
  $('#tableedit').Tabledit({
    url: '/personal/edit',
    restoreButton: true,
    columns: {
      identifier: [0, 'id'],
      editable: [[1, 'label'],
        [2, 'name'],
      [3, 'mail'],
      [4, 'phone'],
      [5, 'street'],
      [6, 'postcode'],
      [7, 'city'],
      [8, 'taxnumber'],
      [9, 'payment_id', '{{!payment_options}}']      
      ]
    },

    onSuccess: function (data, textStatus, jqXHR, lastEditedRow) {
      if (data.new_id) {
        lastEditedRow.attr('id', data.new_id);
        lastEditedRow.find('span.tabledit-span.tabledit-identifier').text(data.new_id);
        lastEditedRow.find('input.tabledit-input.tabledit-identifier').attr('value', data.new_id);
      }
    },
    onFail: function (jqXHR, textStatus, errorThrown) {
      console.log('onFail(jqXHR, textStatus, errorThrown)');
      console.log(jqXHR);
      console.log(textStatus);
      console.log(errorThrown);
      alert(jqXHR.responseText);
    }
  });

  $("#addRow").click(function () {
    var clone = $(".tableedit-template").first().clone();
    clone.show();
    clone.removeAttr("class");
    clone.prependTo("table");

  });

</script>