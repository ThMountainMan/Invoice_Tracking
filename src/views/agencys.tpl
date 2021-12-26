% setdefault('title', 'Agencys')
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
        <button class="btn btn-primary" id="addRow"><i class="fas fa-plus"></i>Add New Agency</button>
        <button type="button" class="btn btn-primary" onClick="window.location.reload();">Reload</button>
      </div>
      <br />

      <div class="alert alert-warning collapse alert-dismissible" role="alert" , id="warning">
        Please make sure that all needed fields are filled !!
      </div>

      <div class="alert alert-warning collapse alert-dismissible" role="alert" , id="warning_number">
        Please enter a valid number for the percentage [ 0 - 100 ] !!
      </div>

      <table class="table table-hover" id="tableedit">
        <thead class="thead-light">
          <tr>
            <th style="display: none"></th>
            <th>Name</th>
            <th>Percentage</th>
          </tr>
        </thead>
        <tbody>
          <tr class="tableedit-template" style="display: none;">
            <td style="display: none"></td>
            <td></td>
            <td></td>
          </tr>
          % for agency in agencys:
          <tr>
            <td style="display: none">{{agency.id}}</td>
            <td>{{agency.name}}</td>
            <td>{{agency.percentage}}</td>
          </tr>
          % end
        </tbody>
      </table>

    </div> <!-- /.panel-body -->
  </div> <!-- /.panel -->
</div> <!-- row -->


<script type="text/javascript">
  $('#tableedit').Tabledit({
    url: '/agencys/edit',
    restoreButton: true,
    columns: {
      identifier: [0, 'id'],
      editable: [[1, 'name'],
      [2, 'percentage']
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
    onAjax: function (action, data, serialize) {
      console.log('onAjax(action, serialize)');
      console.log(action);
      console.log(serialize);

      if (action === 'edit') {

        var values = data.split('&');
        var name = values[1].split('=')[1];
        var percentage = values[2].split('=')[1];
        // check for empty string
        if (!name || !percentage)  {
          $("#warning").fadeTo(3000, 800).slideUp(800, function () {
            $("#warning").slideUp(800);
          });

        return false;
        }
        else if (!Number(percentage)) {
          $("#warning_number").fadeTo(3000, 800).slideUp(800, function () {
            $("#warning_number").slideUp(800);
          });
          return false;
        }
        
        else {
          return true;
        }
      }
    }
  });

  $("#addRow").click(function () {
    var clone = $(".tableedit-template").first().clone();
    clone.show();
    clone.removeAttr("class");
    clone.prependTo("table");

  });

</script>