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

