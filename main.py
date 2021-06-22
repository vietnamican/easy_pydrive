from time import sleep
from auth import get_drive_instance
from api import list_dir, up_files, check_files_exist, up_folder

drive = get_drive_instance()

parent_id = "1Bkoka3pDX60O3oqFKv0P85oiN1SmDpSZ"

# check_files_exist(drive, [1], parent_id)
up_folder(drive, 'folder_a', parent_id)