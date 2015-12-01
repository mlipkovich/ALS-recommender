<?php
$servername = "";
$username = "";
$password = "";
$db = "";

$conn =  mysql_connect($servername, $username, $password);

if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

mysql_select_db($db, $conn);

$query = $_REQUEST['q'];
$movies_arr = explode(',', $query);
$movies_arr = array_map("mysql_real_escape_string", $movies_arr);
$movies_arr = array_map("normalize_title", $movies_arr);
$movies = implode(',', $movies_arr);

$sql = mysql_query("SELECT movie_title, similar_movies FROM suggestions WHERE movie_title IN ($movies)");
echo '<p><b>Movies you will probably like: </b></p>';

while ($row = mysql_fetch_array($sql)) {
  echo '<p>'. $row['similar_movies'] .'</p>';
}

/**
 * Normalizes movie title for using as a key in database (removes "the", commas, etc).
 * Adds trailing quotes for being used in a query.
 */
function normalize_title($title) {

  $title = trim($title);
  $title = strtolower($title);
  if (substr($title, 0, strlen("the ")) === "the ") {
    $title = substr($title, strlen("the "));
  }

  if (substr($title, 0, strlen("a ")) === "a ") {
    $title = substr($title, strlen("a "));
  }

  $title = str_replace(" a ", " ", $title);
  $title = str_replace(" the ", " ", $title);
  $title = str_replace(" & ", " and ", $title);
  $title = str_replace(",", "", $title);
  $title = str_replace(" ", "", $title);
  $title = "'" . $title . "'";
  return $title;
}


?>
