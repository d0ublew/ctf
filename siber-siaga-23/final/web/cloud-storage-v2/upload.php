<?php
error_reporting(E_ALL);
define('UPLOAD_PATH', 'uploads/');

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["image"])) {
    $uploadDir = "uploads/"; 
    $uploadedFile = $uploadDir . basename($_FILES["image"]["name"]);
    $imageFileType = strtolower(pathinfo($uploadedFile, PATHINFO_EXTENSION));

    $check = getimagesize($_FILES["image"]["tmp_name"]);
    if ($check !== false) {
        $file_ext = pathinfo($_FILES["image"]["name"], PATHINFO_EXTENSION);
        $img_path = UPLOAD_PATH . '/' . rand(10, 99) . date("YmdHis") . "." . $file_ext;

        if (move_uploaded_file($_FILES["image"]["tmp_name"], $img_path)) {
            $sourceImage = imagecreatefromstring(file_get_contents($img_path));
            $thumbnailWidth = 150;  
            $thumbnailHeight = 150; 
            $thumbnailImage = imagecreatetruecolor($thumbnailWidth, $thumbnailHeight);
            imagecopyresampled($thumbnailImage, $sourceImage, 0, 0, 0, 0, $thumbnailWidth, $thumbnailHeight, imagesx($sourceImage), imagesy($sourceImage));

            $thumbnailPath = $uploadDir . "thumbnail_" . basename($img_path);
            imagejpeg($thumbnailImage, $thumbnailPath);
            imagedestroy($sourceImage);
            imagedestroy($thumbnailImage);

            echo "File uploaded successfully. Full path: " . realpath($img_path);
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    } else {
        echo "File is not an image.";
    }
}
?>
