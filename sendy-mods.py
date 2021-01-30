#### SET PATH TO SENDY INSTALL HERE ####
folder_path = '/var/www/sendy.dxetech.org/'

from array import *

# modications is a 2d array where each interior array contains 2 values:
# [i][0] is the file to modify, [i][1] is the string to remove
modifications = [
	['login.php', '<p><a href="#forgot-form" title="" data-toggle="modal" class="recovery" id="forgot-btn"><?php echo _(\'Forgot password?\');?></a></p>'],
	['subscribers.php', '<button class="btn" onclick="window.location=\'<?php echo get_app_info(\'path\');?>/includes/subscribers/export-csv.php?i=<?php echo get_app_info(\'app\');?>&l=<?php echo $lid;?>&<?php echo $filter.\'=\'.$filter_val;?>\'"><i class="icon-download-alt"></i> <?php echo _(\'Export\').\' \'.$export_title;?></button>'],
	['segment.php', '<a href="<?php echo get_app_info(\'path\');?>/includes/segments/export-csv.php?i=<?php echo get_app_info(\'app\');?>&l=<?php echo $lid;?>&s=<?php echo $sid;?>" class="export-seg-csv" title="<?php echo _(\'Export CSV of this segment\');?>"><i class="icon icon-download-alt"></i> <?php echo _(\'Export\');?></a>']],
	['subscribe.php', 'update_segments($app_path, $list_id);']
	['confirm.php', 'update_segments($app_path, $list_id);']

adminOnlyPre = '<?php if(!get_app_info(\'is_sub_user\')):?>'
adminOnlyPost = '<?php endif;?>'

for m in modifications:
	# read input file
	fin = open(folder_path + m[0], "rt")
	# read file contents to string
	data = fin.read()
	# string replacment
	newString = ''
	# if not login page, prepend/append it instead of removing it
	if m[0] != 'login.php' | m[0] != 'subscribe.php' | m[0] != 'confirm.php' :
		newString = adminOnlyPre + m[1] + adminOnlyPost;
	data = data.replace(m[1], newString)
	# close the input file
	fin.close()
	# open the input file in write mode
	fin = open(folder_path + m[0], "wt")
	# overrite the input file with the new data
	fin.write(data)
	# close the file
	fin.close()