% setdefault('title', 'Bank Details') % include("base.tpl")
<div class="container-fluid">
  <div class="panel-heading">
    <h1 class="panel-title">
      {{ title }}
    </h1>
  </div>
  <div class="panel-body">
    <div class="clearfix">
      <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#create">
        Add New Payment Method
      </button>
      <button type="button" class="btn btn-primary" onClick="window.location.reload();">
        Reload
      </button>
    </div>
    <br />

    <table class="table table-hover" id="tableedit">
      <thead class="thead-light">
        <tr>
          <td style="display: none"></td>
          <th>Label</th>
          <th>Bank Details</th>
          <th>EDIT</th>
        </tr>
      </thead>

      % for data in input:

      <tr>
        <td style="display: none">{{ data.id }}</td>
        <td>
          <strong>{{ data.label }}</strong>
        </td>
        <td>
          {{ data.name }}<br />
          {{ data.bank }}<br />
          {{ data.IBAN }}<br />
          {{ data.BIC }}<br />
        </td>

        <td>
          <!-- <button onclick="location.href = '/payment_edit/{{data.id}}';" type="button" class="btn btn-warning btn-sm">EDIT</button> -->
          <button type="button" class="btn btn-warning btn-sm" data-toggle="modal"
            data-target="#showdata_{{ data.id }}">
            EDIT
          </button>
          <!-- <button onclick="location.href = '/payment_delete/{{data.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button> -->
        </td>
      </tr>

      <!-- Modal Pop up view for editing purposes -->
      <div class="modal fade" id="showdata_{{ data.id }}" tabindex="-1" role="dialog"
        aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLongTitle">
                Edit Payment Details "{{ data.label }}"
              </h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form class="p-3" method="post" action="/payment_edit/{{ data.id }}" id="form_{{ data.id }}">
                <input type="hidden" id="id" name="id" value="{{ data.id }}" />

                <div class="form-group required">
                  <b><label class="control-label">LABEL:</label></b>
                  <input type="text" id="label" class="form-control" name="label" value="{{ data.label }}" required />
                </div>

                <div class="form-group required">
                  <b><label class="control-label">Name:</label></b>
                  <input type="text" id="name" class="form-control" name="name" value="{{ data.name }}" required />
                </div>

                <div class="form-group">
                  <b><label class="control-label">Bank:</label></b>
                  <input type="text" id="bank" class="form-control" name="bank" value="{{ data.bank }}" required />
                </div>

                <div class="form-group required">
                  <b><label class="control-label">IBAN:</label></b>
                  <input type="text" id="IBAN" class="form-control" name="IBAN" value="{{ data.IBAN }}" required />
                </div>

                <div class="form-group required">
                  <b><label class="control-label">BIC:</label></b>
                  <input type="text" id="BIC" class="form-control" name="BIC" value="{{ data.BIC }}" required />
                </div>

                <div class="modal-footer">
                  <input type="submit" class="btn btn-primary" value="Save Changes" />
                  <button type="button" class="btn btn-secondary" data-dismiss="modal">
                    Close
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        % end
      </div>
    </table>

    <!-- Create a new Payment Entry -->
    <!-- Modal Pop up view for editing purposes -->
    <div class="modal fade" id="create" tabindex="0" role="dialog" aria-labelledby="exampleModalCenterTitle"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">
              Create Payment Details
            </h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form method="post" action="/payment_edit" id="myForm">
              <div class="form-group required">
                <b><label class="control-label">LABEL:</label></b>
                <input type="text" id="label" class="form-control" name="label" required />
              </div>

              <div class="form-group required">
                <b><label class="control-label">Name:</label></b>
                <input type="text" id="name" class="form-control" name="name" required />
              </div>

              <div class="form-group">
                <b><label class="control-label">Bank:</label></b>
                <input type="text" id="bank" class="form-control" name="bank" required />
              </div>

              <div class="form-group required">
                <b><label class="control-label">IBAN:</label></b>
                <input type="text" id="IBAN" class="form-control" name="IBAN" required />
              </div>

              <div class="form-group required">
                <b><label class="control-label">BIC:</label></b>
                <input type="text" id="BIC" class="form-control" name="BIC" required />
              </div>

              <div class="modal-footer">
                <input type="submit" class="btn btn-primary" value="Save Changes" />
                <button type="button" class="btn btn-secondary" data-dismiss="modal">
                  Close
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script type="text/javascript">
  $("#tableedit").Tabledit({
    url: "/payment_edit",
    restoreButton: false,
    editButton: false,
    columns: {
      identifier: [0, "id"],
      editable: [],
    },

    onSuccess: function (data, textStatus, jqXHR, lastEditedRow) {
      if (data.new_id) {
        lastEditedRow.attr("id", data.new_id);
        lastEditedRow
          .find("span.tabledit-span.tabledit-identifier")
          .text(data.new_id);
        lastEditedRow
          .find("input.tabledit-input.tabledit-identifier")
          .attr("value", data.new_id);
      }
    },
    onFail: function (jqXHR, textStatus, errorThrown) {
      console.log("onFail(jqXHR, textStatus, errorThrown)");
      console.log(jqXHR);
      console.log(textStatus);
      console.log(errorThrown);
      alert(jqXHR.responseText);
    },
  });

  $("#addRow").click(function () {
    var clone = $(".tableedit-template").first().clone();
    clone.show();
    clone.removeAttr("class");
    clone.prependTo("table");
  });

  $("form").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var id = form.attr("id");
    // alert(id + ' form submitted');
    $.ajax({
      url: "/payment_edit",
      type: "post",
      data: form.serialize(),
      action: "hallo",
      success: function () {
        // alert("worked");
      },
    });
    window.location.reload();
  });
</script>