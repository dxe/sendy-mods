# sendy-mods
Security modifications for Sendy

Created by Jake Hobbs for DxE on 2020.06.25

## Features:
- Disables "forgot password" option on login page
- Disables "subscriber export" on subscriber list pages for non-admin users
- Disables "subscriber export" on segment pages for non-admin users
- Prevents update_segments function from running each time someone subsribes or confirms their subscription. (We just run this once each day via a cron job to prevent the table from constantly rebuilding.)

## Instructions to perform after each Sendy upgrade:
1. Ensure folder_path is set correctly.
2. Execute the script.
3. Login to Sendy and confirm that all changes were successful

## Using S3 for uploads:
1. Add this to includes/config.php:
```
define('AWS_ACCESS_KEY', 'value');
define('AWS_SECRET_KEY', 'value');
define('S3_ENDPOINT', 'value');
define('S3_BUCKET_NAME', 'value');
```
2. Replace includes/create/upload.php:
```
<?php
    include('../functions.php');
    include('../login/auth.php');
    require_once('../helpers/S3.php');
    
    //Init
    $file = $_FILES['upload']['tmp_name'];
    $fileName = $_FILES['upload']['name'];
    $extension_explode = explode('.', $fileName);
    $extension = $extension_explode[count($extension_explode)-1];
    $extension2 = $extension_explode[count($extension_explode)-2];
    if($extension2=='php' || $file_name=='.htaccess') exit;

    $time = time();

    $allowed = array("jpeg", "jpg", "gif", "png");

    if(in_array(strtolower($extension), $allowed)) {
        $awsAccessKey = AWS_ACCESS_KEY;
        $awsSecretKey = AWS_SECRET_KEY;
        $bucketName = S3_BUCKET_NAME;
        $s3 = new S3($awsAccessKey, $awsSecretKey, false, S3_ENDPOINT);
        $s3Filename = $time . "." . $extension;
        if ($s3 -> putObject($s3->inputFile($file), $bucketName, $s3Filename, S3::ACL_PUBLIC_READ)) {

            // Required: anonymous function reference number as explained above.
            $funcNum = $_GET['CKEditorFuncNum'] ;
            // Optional: instance name (might be used to load a specific configuration file or anything else).
            $CKEditor = $_GET['CKEditor'] ;
            // Optional: might be used to provide localized messages.
            $langCode = $_GET['langCode'] ;

            $url = 'http://'.S3_ENDPOINT.'/'.$bucketName.'/'.$s3Filename;
            // Usually you will only assign something here if the file could not be uploaded.
            $message = '';

            echo "<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction($funcNum, '$url', '$message');</script>";
        }
        else exit;
    }
    else exit;
?>
```
3. Add S3.php file to includes/helpers/

## Additional hacks
### Allow segmentation by relative date
1. Add to includes/segments/main.php:
```
else if($com=='WITHIN_DAYS') //within last days
{
    $now = strtotime('now');
    $date_start = $now - ($needle * 86400);

    if($haystack > $date_start)
        push_into_cf_hold_array($sid);
}
```
2. Manually update the seg_cons table in the database using "WITHIN_DAYS" as the comparison and the number of days as the val. Note that these will not be visible in the UI, but it will work.
