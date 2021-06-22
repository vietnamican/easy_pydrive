from time import sleep
from auth import get_drive_instance
from api import list_dir

drive = get_drive_instance()

file_list = list_dir(drive, "1Q1pHCMRR0YcjfZjWWlOrVO4FGr7LUHzs")
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))