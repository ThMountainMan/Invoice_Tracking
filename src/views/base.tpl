<!DOCTYPE html>
<html>
<head>
<style>
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
  <li><a class="active" href="/">Start</a></li>
  <li><a href="/customers">Customers</a></li>
  <li><a href="/jobtypes">Jobtypes</a></li>
  <li><a href="/agencys">Agencys</a></li>
</ul>

</body>
</html>
