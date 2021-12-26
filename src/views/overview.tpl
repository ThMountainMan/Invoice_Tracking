<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
    <meta charset="utf-8">
    <title>Invoice Tracker</title>
    <style>
    </style>
</head>

<body>
    <h1 class="logo">Total Overview - {{year}} </h1>

    <table class="table" id="cssTable">
        <thead class="thead-light">
            <tr>
                <th class="align-center">Income</th>
                <th class="align-cente">Outstanding</th>
                <th class="align-center">Expenses</th>
                <th class="align-center">Profit</th>
        </thead>
        </tr>
        <tr>
            <td class="table-success"><b>€ {{"{:.2f}".format(income)}}</b></td>
            % if outstanding > 0:
            <td class="table-warning"><b>€ {{"{:.2f}".format(outstanding)}}</b></td>
            %else:
            <td class="table-warning"><b>€ {{"{:.2f}".format(outstanding)}}</b></td>
            %end
            <td class="table-danger"><b>€ {{"{:.2f}".format(expenses)}}</b></td>
            % if profit >= 0:
            <td class="table-success"><b>€ {{"{:.2f}".format(profit)}}</b></td>
            %else:
            <td class="table-danger"><b>€ {{"{:.2f}".format(profit)}}</b></td>
            %end
        </tr>
    </table>

    <!-- <h1 class="logo">All available invoices </h1>
    
    <div class="row">
        <div class="col-sm-2 form-inline">
            <label for="filter_year" class="col-lg-4">Year:</label>
            <select name="filter_year" class="form-control w-100" id="dropdownYear" style="width: 120px;"
                onchange="location = this.value;">
                <option value="/invoices" selected>ALL</option>
                <option value="/invoices/2020">2020</option>
                <option value="/invoices/2021">2021</option>
            </select>
        </div>
        <div class="col-sm-2">
            <label for="filter_jobtype">Jobtypes:</label>
            <select name="filter_jobtype" class="form-control w-100" id="filter_jobtype" style="width: 120px;"
                onchange="location = this.value;" disabled>
                <option value="/invoices" selected>--</option>
                % for jobtype in jobtypes:
                <option value="/invoices_filter/jobytpes/{{jobtype.id}}">{{jobtype.name}}</option>
                % end
            </select>
        </div>
        <div class=" col-sm-2">
            <label for="filter_status">Status:</label>
            <select name="filter_status" class="form-control w-100" id="filter_status" style="width: 120px;"
                onchange="location = this.value;" disabled>
                <option value="/invoices" selected>--</option>
                <option value="/invoices_filter/status/1">OPEN</option>
                <option value="/invoices_filter/status/2">PAYED</option>
            </select>
        </div>
    
    </div> -->


</body>

<script>
    // //
    // // This Script adds all the years to the Year Selector
    // //
    // var i, currentYear, startYear, endYear, newOption, dropdownYear;
    // var pathArray = window.location.pathname.split('/');
    // dropdownYear = document.getElementById("dropdownYear");
    // currentYear = (new Date()).getFullYear();
    // startYear = 2010;
    // endYear = currentYear;

    // document.getElementById('currentYear').innerHTML = pathArray[2];

    // for (i = startYear; i <= endYear; i++) {
    //     newOption = document.createElement("option");
    //     newOption.value = "/invoices/" + i;
    //     newOption.label = i;
    //     if (i == pathArray[2]) {
    //         newOption.selected = true;
    //     }
    //     dropdownYear.appendChild(newOption);
    // }

    </script>