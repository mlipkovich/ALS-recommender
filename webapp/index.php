<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="styles/common.css">
</head>
<body>

<div>
<form id="searchbox" action="index.php">
    <input id="search" type="text" placeholder="Type your favourite movies here" name="q">
    <input id="submit" type="submit" value="Recommend">
</form>
</div>

<div style="position:relative">
    <center><img src="images/film.jpeg"></center>
</div>


<div id="suggestions">
<?php
if (!empty($_REQUEST['q'])) {
  include 'search.php';
}
?>
</div>

</body>
</html>

