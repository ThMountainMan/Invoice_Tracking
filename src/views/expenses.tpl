% setdefault('title', 'Expenses')
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
        <button class="btn btn-primary" id="addRow"><i class="fas fa-plus"></i>Add New Expense</button>
        <button type="button" class="btn btn-primary" onClick="window.location.reload();">Reload</button>
      </div>
      <br />

      <div class="alert alert-warning collapse alert-dismissible" role="alert" , id="warning">
        Please make sure that all fields are filled!!
      </div>


      <table class="table table-hover" id="tableedit">
        <thead class="thead-light">
          <tr>
            <th style="display:none;"></th>
            <th>ID</th>
            <th>Date</th>
            <th>Cost</th>
            <th>Comment</th>
          </tr>
        </thead>
        <tbody>
          <tr class="tableedit-template" style="display: none;">
            <td style="display:none;"></td>
            <td></td>
            <td><div><input type="date" name="date" required /></div></td>
            <td></td>
            <td></td>
          </tr>
          % for expense in expenses:
          <tr>
            <td style="display:none;">{{expense.id}}</td>
            <td>{{expense.expense_id}}</td>
            <td>{{expense.date}}</td>
            <td>{{expense.cost}}</td>
            <td>{{expense.comment}}</td>
          </tr>
          % end
        </tbody>
      </table>

    </div> <!-- /.panel-body -->
  </div> <!-- /.panel -->
</div> <!-- row -->


<script type="text/javascript">
  $('#tableedit').Tabledit({
    url: '/expenses/edit',
    restoreButton: true,
    autoFocus: false,
    columns: {
      identifier: [0, 'id'],
      editable: [[2, 'date'],
      [3, 'cost'],
      [4, 'comment']
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
    },
    onDraw: function () {
      // Select all inputs of second column and apply datepicker each of them
      $('table tr td:nth-child(3) input').each(function () {
        $(this).datepicker({
          format: 'dd-mm-yyyy',
          todayHighlight: true,
          disabled: false
        });
      });
    },

    onAjax: function (action, data, serialize) {
      console.log('onAjax(action, serialize)');
      console.log(action);
      console.log(serialize);

      if (action === 'edit') {

        var values = data.split('&');
        var date = values[1].split('=')[1];
        var cost = values[2].split('=')[1];
        var comment = values[3].split('=')[1];

        // check for empty string
        if (!date || !cost || !comment) {
          $("#warning").fadeTo(3000, 800).slideUp(800, function () {
            $("#warning").slideUp(800);
          });
          return false;
        } else {
          return true;
        }
      }
    }

  });

  $("#addRow").click(function () {
    var clone = $(".tableedit-template").first().clone(false, false);
    clone.show();
    clone.removeAttr("class");
    clone.prependTo("table");
  });
</script>