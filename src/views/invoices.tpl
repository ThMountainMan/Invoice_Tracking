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
      background-color: #FBFF93
    }

    form {
      margin: 0px;
      padding: 0px;
      display: inline;
    }

    p {
      margin: 0;
      display: inline;
      float: center;
    }
  </style>
</head>

<body>
  % include('base.tpl')
  <header>
    <div class="container-fluid">
      <h1 class="logo">Total Overview <p id="currentYear"></p>
      </h1>

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
          <td><b>€ {{overview['income']}}</b></td>
          % if overview['outstanding'] > 0:
          <td class="open"><b>€ {{overview['outstanding']}}</b></td>
          %else:
          <td><b>€ {{overview['outstanding']}}</b></td>
          %end
          <td><b>€ {{overview['expenses']}}</b></td>
          % if overview['profit'] >= 0:
          <td class="positive"><b>€ {{overview['profit']}}</b></td>
          %else:
          <td class="negative"><b>€ {{overview['profit']}}</b></td>
          %end
        </tr>
      </table>

      <br>

      <div>
        <h1 class="logo">All available invoices </h1>

        <div class="row">
          <div class="col-sm-2 form-inline">
            <label for="filter_year" class="col-lg-4">Year:</label>
            <select name="filter_year" class="form-control w-100" id="dropdownYear" style="width: 120px;" onchange="location = this.value;">
              <option value="/invoices" selected>ALL</option>
            </select>
          </div>
          <div class="col-sm-2">
            <label for="filter_jobtype">Jobtypes:</label>
            <select name="filter_jobtype" class="form-control w-100" id="filter_jobtype" style="width: 120px;" onchange="location = this.value;" disabled>
              <option value="/invoices" selected>--</option>
              % for jobtype in jobtypes:
              <option value="/invoices_filter/jobytpes/{{jobtype.id}}">{{jobtype.name}}</option>
              % end
            </select>
          </div>
          <div class=" col-sm-2">
            <label for="filter_status">Status:</label>
            <select name="filter_status" class="form-control w-100" id="filter_status" style="width: 120px;" onchange="location = this.value;" disabled>
              <option value="/invoices" selected>--</option>
              <option value="/invoices_filter/status/1">OPEN</option>
              <option value="/invoices_filter/status/2">PAYED</option>
            </select>
          </div>

        </div>


        <br>
        <br><a href="/invoice_add" class="btn btn-primary"> Create New Invoice </a><br><br>
        <table class=" table" id="invoices">
          <thead class="thead-light">
            <tr>
              <th onclick="sortTable(0)">Invoide ID</th>
              <th onclick="sortTable(1)">Invoice Date</th>
              <th onclick="sortTable(2)">Customer Name</th>
              <th onclick="sortTable(3)">Job Type</th>
              <th onclick="sortTable(4)">Ammount</th>
              <th onclick="sortTable(5)">Paydate</th>
              <th>Download / EDIT</th>
          </thead>
          </tr>
          % for invoice in input:
          % if invoice.paydate:
          <tr style="background-color:#F6FFF6;">
            % else:
          <tr style=" background-color: #FBFF93;">
            % end
            <td><b><a href="/invoice_show/{{invoice.id}}">{{invoice.invoice_id}}</a></b></td>
            <td>{{invoice.date}}</td>
            <td>{{invoice.customer.name}}</td>
            <td>{{invoice.jobtype.name}}</td>
            <td><b> € {{invoice.invoice_ammount}}</b></td>
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
              <form action="/invoice_show/{{invoice.id}}" method="post">
                <button type="submit" class="btn btn-primary btn-sm"><i class="fa fa-download"></i></button>
              </form>

              <button onclick="location.href = '/invoice_edit/{{invoice.id}}';" type="button" class="btn btn-warning btn-sm">EDIT</button>
              <!--<button href="/invoice_delete/{{invoice.id}}" onclick="return confirm('Are you sure?');" type="button" class="btn btn-danger btn-sm">DELETE</button> -->
              <a href="/invoice_delete/{{invoice.id}}" class="btn btn-danger btn-sm" onclick="return confirm('Are you sure you want to delete the Invoice:\n--> {{invoice.invoice_id}}?')">DELETE</a>
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

    document.getElementById('currentYear').innerHTML = pathArray[2];

    for (i = startYear; i <= endYear; i++) {
      newOption = document.createElement("option");
      newOption.value = "/invoices/" + i;
      newOption.label = i;
      if (i == pathArray[2]) {
        newOption.selected = true;
      }
      dropdownYear.appendChild(newOption);
    }


    function sortTable(n) {
      var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
      table = document.getElementById("invoices");
      switching = true;
      //Set the sorting direction to ascending:
      dir = "asc";
      /*Make a loop that will continue until
      no switching has been done:*/
      while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /*Loop through all table rows (except the
        first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
          //start by saying there should be no switching:
          shouldSwitch = false;
          /*Get the two elements you want to compare,
          one from current row and one from the next:*/
          x = rows[i].getElementsByTagName("TD")[n];
          y = rows[i + 1].getElementsByTagName("TD")[n];
          /*check if the two rows should switch place,
          based on the direction, asc or desc:*/
          if (dir == "asc") {
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
              //if so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          } else if (dir == "desc") {
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
              //if so, mark as a switch and break the loop:
              shouldSwitch = true;
              break;
            }
          }
        }
        if (shouldSwitch) {
          /*If a switch has been marked, make the switch
          and mark that a switch has been done:*/
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
          //Each time a switch is done, increase this count by 1:
          switchcount++;
        } else {
          /*If no switching has been done AND the direction is "asc",
          set the direction to "desc" and run the while loop again.*/
          if (switchcount == 0 && dir == "asc") {
            dir = "desc";
            switching = true;
          }
        }
      }
    }
  </script>

</body>

</html>