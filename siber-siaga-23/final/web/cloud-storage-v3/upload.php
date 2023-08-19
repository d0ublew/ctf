<?php
$size = array(
    "width" => 32,
    "height" => 32
);

$dir = "uploads/";

if (isset($_FILES['upload']) && $_FILES['upload']['error'] === 0) {
    $check = getimagesize($_FILES["upload"]["tmp_name"]);

    $file_extension = pathinfo($_FILES["upload"]["name"], PATHINFO_EXTENSION);

    if (!file_exists($_FILES["upload"]["tmp_name"])) {
        $response = array(
            "type" => "error",
            "message" => "Choose an image file to upload."
        );
    } else if ($_FILES["upload"]["size"] > 2000000) {
        $response = array(
            "type" => "error",
            "message" => "Image size exceeds 2MB"
        );
    } else {
        $target = imagecreatetruecolor($size['width'], $size['height']);

        imagecopyresampled($target, imagecreatefromstring(file_get_contents($_FILES["upload"]["tmp_name"])), 0, 0, 0, 0, $size['width'], $size['height'], $check[0], $check[1]);
        $random_number = rand(1000, 9999);

        $newFileName = time() . "_" . $random_number . "." . $file_extension;

        $uploadPath = $dir . $newFileName;

        if (imagepng($target, $uploadPath)) {
            $response = array(
                "type" => "success",
                "message" => "Image uploaded successfully.",
                "path" => $uploadPath
            );
        } else {
            $response = array(
                "type" => "error",
                "message" => "Problem in uploading image files."
            );
        }
    }
} else {
    $response = array(
        "type" => "error",
        "message" => "No file provided."
    );
}

echo $response['type'] . ": " . $response['message'];

if (isset($response['path'])) {
    echo " Path: " . $response['path'];
}
?>
