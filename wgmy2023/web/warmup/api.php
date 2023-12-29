<?php

error_reporting(0);

if (!isset($_GET['x'])) {
    header('Location: /?x=flag.php');
    die();
}

$x = $_GET['x'];

if (preg_match('/(?:data|file|ftp|http|input|phar|convert|string|proc|fd)/', $x, $m)) {
    die('did you just mention "' . $m[0] . '"?? i\'m quitting now');
}

include_once $x;
?>
