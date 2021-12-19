% setdefault('title', 'Customers')
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
            <th>#</th>
            <th>Name</th>
            <th>Contact Person</th>
            <th>Contact Mail</th>
            <th>Contact Phone</th>
            <th>Street</th>
            <th>Postcode</th>
            <th>City</th>
            <th>Country</th>
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
          </tr>
            % for customer in input:
            <tr>
              <td>{{customer.id}}</td>
              <td>{{customer.name}}</td>
              <td>{{customer.contact}}</td>
              <td>{{customer.email}}</td>
              <td>{{customer.phone}}</td>
              <td>{{customer.street}} </td>
              <td>{{customer.postcode}}</td>
              <td>{{customer.city}} </td>
              <td>{{customer.country}}</td>
              </tr>
              % end
        </tbody>
      </table>

    </div> <!-- /.panel-body -->
  </div> <!-- /.panel -->
</div> <!-- row -->


<script type="text/javascript">
  $('#tableedit').Tabledit({
    url: '/customers/edit',
    restoreButton: true,
    columns: {
      identifier: [0, 'id'],
      editable: [[1, 'name'],
      [2, 'contact'],
      [3, 'email'],
      [4, 'phone'],
      [5, 'street'],
      [6, 'postcode'],
      [7, 'city'],
      [8, 'country']
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