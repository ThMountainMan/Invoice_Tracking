<!DOCTYPE html>
<html>


<link rel="stylesheet" type="text/css" href="/static/css/bootstrap.css">
<script src="/static/jquery-3.2.1.slim.min.js"></script>
<script src="/static/bootstrap.min.js"></script>
<link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">

<head>
  <style>
  </style>
</head>

<body>

  <nav class="navbar navbar-light navbar-expand-lg navbar-light bg-light" style="background-color: #e3f2fd;">
    <a class="navbar-brand" href="/">Invoice Tracker</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">

        <li class="nav-item">
          <a class="nav-link" href="/"> Invoices </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/expenses"> Expenses </a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Setup Section
          </a>
          <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" href="/personal">Personal Details</a>
            <a class="dropdown-item" href="/payment">Bank Details</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="/customers">Customers</a>
            <a class="dropdown-item" href="/jobtypes">Jobtypes</a>
            <a class="dropdown-item" href="/agencys">Agencys</a>
          </div>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Filter</a>
        </li>
      </ul>
      <form class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
      </form>
    </div>
  </nav>

  <br>
</body>

</html>