% setdefault('title', 'Customers') %include("base.tpl")

<body>
  <div class="container-fluid">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h1 class="panel-title">
          {{ title }}
        </h1>
      </div>
      <div class="panel-body">
        <div class="clearfix">
          <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#create"><i class="fas fa-plus"></i>
            Add New Customer
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
              <th>Name</th>
              <th>Contact Person</th>
              <th>Contact Details</th>
              <th>Address</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr class="tableedit-template" style="display: none">
              <td style="display: none"></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
            </tr>
            % for customer in input:
            <tr>
              <td style="display: none">{{ customer.id }}</td>
              <td>{{ customer.name }}</td>
              <td>{{ customer.contact }}</td>
              <td>
                {{ customer.email }} <br />
                {{ customer.phone }}
              </td>
              <td>
                {{ customer.street }} <br />
                {{ customer.postcode }}<br />
                {{ customer.city }} <br />
                {{ customer.country }}
              </td>
              <td align="right">
                <button type="button" class="button btn btn-warning btn-sm" data-toggle="modal"
                  style="margin-right:-25px;" data-target="#showdata_{{ customer.id }}"><i
                    class="fas fa-edit"></i></button>
              </td>
            </tr>

            <!-- EDIT existing Customer -->
            <div class="modal fade" id="showdata_{{ customer.id }}" tabindex="0" role="dialog"
              aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLongTitle">
                      Edit Customer Details "{{ customer.name }}"
                    </h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                  <div class="modal-body">
                    <form method="post" action="/payment_edit" id="form_{{ customer.id }}">

                      <input type="hidden" name="id" value="{{ customer.id }}" />

                      <div class="form-group required">
                        <b><label class="control-label">Name:</label></b>
                        <input type="text" class="form-control" name="name" required value="{{ customer.name }}" />
                      </div>

                      <div class="form-group required">
                        <b><label class="control-label">Contact Person:</label></b>
                        <input type="text" class="form-control" name="contact" required
                          value="{{ customer.contact }}" />
                      </div>

                      <div class="form-group">
                        <b><label class="control-label">E-Mail Contact:</label></b>
                        <input type="email" class="form-control" name="email" required value="{{ customer.email }}" />
                      </div>

                      <div class="form-group required">
                        <b><label class="control-label">Phone Number:</label></b>
                        <input type="text" class="form-control" name="phone" required value="{{ customer.phone }}" />
                      </div>

                      <div class="form-group required">
                        <b><label class="control-label">Street:</label></b>
                        <input type="text" class="form-control" name="street" required value="{{ customer.street }}" />
                      </div>

                      <div class="form-row">
                        <div class="col-md-6 mb-3">
                          <div class="form-group required">
                            <b><label class="control-label">City:</label></b>
                            <input type="text" class="form-control" name="city" required value="{{ customer.city }}" />
                          </div>
                        </div>

                        <div class="col-md-3 mb-3">
                          <div class="form-group required">
                            <b><label class="control-label">Postcode:</label></b>
                            <input type="text" class="form-control" name="postcode" required
                              value="{{ customer.postcode }}" />
                          </div>
                        </div>
                      </div>

                      <div class="form-group required">
                        <b><label class="control-label">Country:</label></b>
                        <input type="text" class="form-control" name="country" required
                          value="{{ customer.country }}" />
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


            % end
          </tbody>
        </table>
      </div>
      <!-- /.panel-body -->
    </div>
    <!-- /.panel -->
  </div>
  <!-- row -->

  <!-- Create new Customer -->
  <div class="modal fade" id="create" tabindex="0" role="dialog" aria-labelledby="exampleModalCenterTitle"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLongTitle">
            Create New Customer
          </h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form method="post" action="/payment_edit" id="myForm">
            <div class="form-group required">
              <b><label class="control-label">Name:</label></b>
              <input type="text" class="form-control" name="name" required />
            </div>

            <div class="form-group required">
              <b><label class="control-label">Contact Person:</label></b>
              <input type="text" class="form-control" name="contact" required />
            </div>

            <div class="form-group">
              <b><label class="control-label">E-Mail Contact:</label></b>
              <input type="email" class="form-control" name="email" required />
            </div>

            <div class="form-group required">
              <b><label class="control-label">Phone Number:</label></b>
              <input type="text" class="form-control" name="phone" required />
            </div>

            <div class="form-group required">
              <b><label class="control-label">Street:</label></b>
              <input type="text" class="form-control" name="street" required />
            </div>

            <div class="form-row">
              <div class="col-md-6 mb-3">
                <div class="form-group required">
                  <b><label class="control-label">City:</label></b>
                  <input type="text" class="form-control" name="city" required />
                </div>
              </div>

              <div class="col-md-3 mb-3">
                <div class="form-group required">
                  <b><label class="control-label">Postcode:</label></b>
                  <input type="text" class="form-control" name="postcode" required />
                </div>
              </div>
            </div>

            <div class="form-group required">
              <b><label class="control-label">Country:</label></b>
              <input type="text" class="form-control" name="country" required value="Germany" />
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
</body>






<script type="text/javascript">

  $("#tableedit").Tabledit({
    url: "/customers/edit",
    restoreButton: true,
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

  $("form").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var id = form.attr("id");
    // alert(id + ' form submitted');
    $.ajax({
      url: "/customers/edit",
      type: "post",
      data: form.serialize() + "&action=edit",
      success: function () {
        // alert("worked");
      },
    });
    window.location.reload();
  });

</script>