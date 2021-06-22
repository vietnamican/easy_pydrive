from time import sleep
from auth import get_drive_instance
from api import list_dir, up_files, check_files_exist

drive = get_drive_instance()


parent_id = "1Bkoka3pDX60O3oqFKv0P85oiN1SmDpSZ"

# up_files(drive, [1], parent_id)
check_files_exist(drive, [1], parent_id)

# file_list = list_dir(drive, parent_id)
# print(file_list[0])
# for file1 in file_list:
#     print('title: %s, id: %s' % (file1['title'], file1['id']))