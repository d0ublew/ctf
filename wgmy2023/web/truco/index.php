 <?php
include "flag.php";
highlight_file(__FILE__); 
error_reporting(0); 

$a = $_GET['a'];
$b = $_GET['b'];

var_dump($a);
echo "<br>";
var_dump($_SERVER['REQUEST_URI']);

if(!preg_match("/\?a=notnull/i", $_SERVER['REQUEST_URI'])){
    exit("<h2>Oops :(<h2>");
}

if(preg_match("/^[0-9+-\/\*e ]/i", $num)){
    exit("<h2>Oops Oops :(<h2>");
}

echo "<br>";
var_dump($num);
echo "<br>";
var_dump($b);

if (is_null($a)){
    if (is_numeric($num)){
        echo $flag;
    }
    else{
        echo "<h2>No flag for you yet :P<h2>";
    }
}else{
    echo "<h2>No flag for you :P<h2>";
}
?>
