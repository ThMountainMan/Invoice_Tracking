<!DOCTYPE html>
<html>

<link rel="stylesheet" type="text/css" href="/static/style.css">
<script src="/static/jquery-3.2.1.slim.min.js"></script>
<script src="/static/bootstrap.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
<link href="http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">

<head>
  <style>
    /* Make sure that the Container stretches to full width on screen*/
    .container {
      position: absolute;
      width: 100%;
      left: 0;
    }

    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
      border: 1px solid #e7e7e7;
      background-color: #f3f3f3;
    }

    li {
      float: left;
    }

    li a {
      display: block;
      color: #666;
      text-align: center;
      padding: 14px 16px;
      text-decoration: none;
    }

    li a:hover:not(.active) {
      background-color: #ddd;
    }

    li a.active {
      color: white;
      background-color: #4CAF50;
    }
  </style>
</head>

<body>

  <ul>
    <li><a class="active" href="/">INVOICES</a></li>
    <li><a href="/customers">CUSTOMERS</a></li>
    <li><a href="/jobtypes">JOBTYPES</a></li>
    <li><a href="/agencys">AGENCYS</a></li>
  </ul>
  <br>
</body>

</html>