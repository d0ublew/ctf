<?php

require_once __DIR__."/router.php";

$menu = "";

if(isset($_GET["menu"])) {
    $menu = $_GET["menu"];
}

get('/', "landing");
get('/readpdf', 'readpdf');
get('/menu', $menu);
get('/login', 'login');
post('/postlogin', 'authenticate');
get('/home', 'home');
get('/profile', 'profile');
post('/uploadimage', 'uploadimage');

get('/logout', 'logout');<br />
<b>Notice</b>:  ob_flush(): Failed to flush buffer. No buffer to flush in <b>/var/www/html/readpdf.php</b> on line <b>16</b><br />
