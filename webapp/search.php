<?php
$conf = parse_ini_file('../config.ini');
$servername = $conf['host'];
$username = $conf['user'];
$password = $conf['passwd'];
$db = $conf['db'];
$suggests_count = $conf['suggests_count'];

$conn =  mysql_connect($servername, $username, $password);

if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

mysql_select_db("movielens", $conn);

$query = $_REQUEST['q'];
$movies_arr = explode(',', $query);
$movies_arr = array_map("mysql_real_escape_string", $movies_arr);
$movies_arr = array_map("normalize_title", $movies_arr);
$movies = implode(',', $movies_arr);

echo "<p><b>Your query:</b> $query</p>";

$sql = mysql_query("SELECT DISTINCT m.title
  		            FROM normalized_movies AS n
		              INNER JOIN similarities AS s
		                ON n.movie_id = s.movie_id_from
		              INNER JOIN movies m
		                ON s.movie_id_to = m.id
		            WHERE n.normalized_title IN ($movies)
		            ORDER BY s.similarity DESC
		            LIMIT $suggests_count");

if (mysql_num_rows($sql)!=0) {
  echo "<p><b>Movies you will probably like: </b></p>";

  while ($row = mysql_fetch_array($sql)) {
    echo '<p>' . $row['title'] . '</p>';
  }
} else {
  echo "<p><b>No results found for your query</b></p>";
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
