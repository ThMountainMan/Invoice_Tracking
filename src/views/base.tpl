<!DOCTYPE html>
<html lang="en">

<!--We need to include the Bootstrap project in order to use it in our app-->
<!--This shuold fulfill all our needs-->

<!-- https://getbootstrap.com/docs/4.6/getting-started/introduction/ -->



<!-- <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script> -->

<head>
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css"
      integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
</head>

<body>
 
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
  
  <!-- Tableedit -->
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js"></script>
  <script src="static/js/jquery-tabledit/jquery.tabledit.js" ></script>



  
  
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
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
        <input class="form-control mr-sm-2" type="search" id="myInput" onkeyup="myFunction()" placeholder="Search for Invoice ID.." title="Type in a name">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
      </form>
    </div>
  </nav>

  <br>
</body>
<script>
  $(document).ready(function () {
    $(".dropdown-toggle").dropdown();
  });
</script>

</html>