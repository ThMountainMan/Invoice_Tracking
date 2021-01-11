<!DOCTYPE html>
<html lang="en" dir="ltr">

<head>
  <meta charset="utf-8">
  <title>CCC Tracker</title>
  <style>
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }

    td,
    th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }

    tr:nth-child(even) {
      background-color: #dddddd;
    }
  </style>
</head>

<body>
  % include('base.tpl')
  <header>
    <div class="container">
      <h1 class="logo">Agencys</h1>
      <table>
        <tr>
          <th>Name</th>
          <th>Percentage</th>

        </tr>
        % for agency in input:
        <tr>
          <td>{{agency.name}}</td>
          <td>{{agency.percentage}}</td>
          <td> <button style="font-size:24px">EDIT<i class="fa fa-edit"></i></button> </td>
        </tr>
        % end


    </div>
  </header>


</body>

</html>