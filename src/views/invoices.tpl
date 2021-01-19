<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
  <meta charset="utf-8">
  <title>Invoice Tracker</title>
  <style>
    .negative {
      background-color: #ff5c5c
    }

    .positive {
      background-color: #a1ffac
    }

    .open {
      background-color: #FBFF9E
    }

    form {
      margin: 0px;
      padding: 0px;
      display: inline;
    }
  </style>
</head>

<body>
  % include('base.tpl')
  <header>
    <div class="container">
      <h1 class="logo">Overview</h1>

      <table class=" table" id="cssTable">
        <thead class="thead-light">
          <tr>
            <th class="align-center">Income</th>
            <th class="align-center">Outstanding</th>
            <th class="align-center">Expenses</th>
            <th class="align-center">Profit</th>
        </thead>
        </tr>
        <tr>
          <td>€ {{overview['income']}}</td>
          <td>€ {{overview['outstanding']}}</td>
          <td>€ {{overview['expenses']}}</td>
          % if overview['income'] - overview['expenses'] > 0:
          <td class="posivie">€ {{overview['income'] - overview['expenses']}}</td>
          %else:
          <td class="negative">€ {{overview['income'] - overview['expenses']}}</td>
          %end
        </tr>
      </table>

      <div>
        <h1 class="logo">All available invoices </h1>

        <div class="row">
          <div class="col-sm-2 form-inline">
            <label for="filter_year" class="col-lg-4">Year:</label>
            <select name="filter_year" class="form-control w-100" id="dropdownYear" style="width: 120px;" onchange="location = this.value;"></select>
          </div>
          <div class="col-sm-2">
            <label for="filter_jobtype">Jobtype:</label>
            <select name="filter_jobtype" class="form-control w-100" id="filter_jobtype" style="width: 120px;" onchange="location = this.value;"></select>
          </div>
          <div class="col-sm-2">
            <label for="filter_status">Status:</label>
            <select name="filter_status" class="form-control w-100" id="filter_status" style="width: 120px;" onchange="location = this.value;"></select>
          </div>

        </div>


        <br>
        <br><a href="/invoice_add" class="btn btn-primary"> Create New Invoice </a><br><br>
        <table class=" table">
          <thead class="thead-light">
            <tr>
              <th>Invoide ID</th>
              <th>Invoice Date</th>
              <th>Customer Name</th>
              <th>Job Type</th>
              <th>Ammount</th>
              <th>Paydate</th>
              <th>Download</th>
          </thead>
          </tr>
          % for invoice in input:
          % if invoice.paydate:
          <tr>
            % else:
          <tr style="background-color: #FBFF93;">
            % end
            <td><a href="/invoice_show/{{invoice.id}}">{{invoice.invoice_id}}</a></td>
            <td>{{invoice.date}}</td>
            <td>{{invoice.customer.name}}</td>
            <td>{{invoice.jobtype.name}}</td>
            <td>{{invoice.invoice_ammount}} €</td>
            % if invoice.paydate:
            <td>{{invoice.paydate}}</td>
            %else:
            <td>
              <form class="p-3" method="post" action='/invoice_pay/{{invoice.id}}'>
                <div class="pull-left" style="margin-right:10px">
                  <input type="date" id="date" class="form-control" name="date" required>
                </div>
                <button type="submit" class="btn btn-primary btn-sm"><i class="fa fa-check"></i></button>
              </form>
            </td>
            %end
            <td>
              <button class="btn btn-primary btn-sm"><i class="fa fa-download"></i></button>
              <button onclick="location.href = '/invoice_delete/{{invoice.id}}';" type="button" class="btn btn-danger btn-sm">DELETE</button>
            </td>
          </tr>
          % end
        </table>

      </div>
  </header>


  <script>
    //
    // This Script adds all the years to the Year Selector
    //
    var i, currentYear, startYear, endYear, newOption, dropdownYear;
    var pathArray = window.location.pathname.split('/');
    dropdownYear = document.getElementById("dropdownYear");
    currentYear = (new Date()).getFullYear();
    startYear = currentYear - 3;
    endYear = currentYear;

    for (i = startYear; i <= endYear; i++) {
      newOption = document.createElement("option");
      newOption.value = "/invoices/" + i;
      newOption.label = i;
      if (i == pathArray[2]) {
        newOption.selected = true;
      }
      dropdownYear.appendChild(newOption);
    }
  </script>

</body>

</html>