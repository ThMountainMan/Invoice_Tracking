% setdefault('title', 'Projects')
<!-- % rebase('base.tpl') -->
%include("base.tpl")
<div class="row col-md-8 col-md-offset-2">
  <div class="panel panel-default">
    <div class="panel-heading">
      <h3 class="panel-title">
        {{title}}
      </h3>
    </div>
    <div class="panel-body">
      <div class="clearfix">
        <button class="btn btn-primary btn-sm pull-right" id="addRow">Add Row</button>
        <button type="button" class="btn btn-primary btn-sm pull-right page-reload"
          style="margin-right:20px;">Reload</button>
      </div>
      <br />

      <table class="table table-striped table-bordered table-hover" id="tableedit">
        <thead>
          <tr>
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
            <td></td>
            <td></td>
            <td></td>
          </tr>
          % for expense in input:
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
    columns: {
      identifier: [0, 'id'],
      editable: [[1, 'expense_id'],
      [2, 'date'],
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
    }
  });

  $("#addRow").click(function () {
    var clone = $(".tableedit-template").first().clone();
    clone.show();
    clone.removeAttr("class");
    clone.prependTo("table");

  });
</script>
