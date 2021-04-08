# Steps for onboarding a new chapter in Sendy

## Set up list for new signups
1. Create a new brand in Sendy.
2. Create a new list for the brand.
3. Add custom fields to the list (FirstName, Zip, City, State, Phone).
4. Add the List ID and Radius to the ADB.
5. Test that new petition signups are added to the list.

## Add existing global subscribers
1. Make a list of zip codes to add existing subscribers to the list.
2. Query the Sendy database to find people in those zip codes and export to CSV.
```
select
	name,
	email,
    SUBSTRING_INDEX((SUBSTRING_INDEX(custom_fields, '%s%', 6)), '%s%', -1) as zip,
    SUBSTRING_INDEX((SUBSTRING_INDEX(custom_fields, '%s%', 10)), '%s%', -1) as chapter
from
	sendy2021.subscribers
where
	list = 2
	and subscribers.bounced = 0
	and subscribers.unsubscribed = 0
	and subscribers.bounce_soft = 0
	and subscribers.complaint = 0
	and SUBSTRING_INDEX((SUBSTRING_INDEX(custom_fields, '%s%', 6)), '%s%', -1) in (
		"90014","90013","90071","90030" # UPDATE THIS LIST
	);
```
3. Edit the CSV to set the Chapter value to match the ADB.
4. Import the CSV back into the Sendy GLOBAL list to update their Chapter. (IMPORTANT: Leave all other fields except name & email blank to skip updating them.)
5. Make a temporary segment on the Global list to find everyone with their Chapter value set to the new chapter. Export it to CSV, then delete the segment.
6. Import the CSV into the new chapter's list for their own brand.
7. Send onboarding instructions to an organizer from the chapter.
