import pydrive

def list_dir(drive, dir_id):
    query = {
        'supportsAllDrives': True,
        'q': "'{}' in parents and trashed=false".format(dir_id)
    }
    file_list = drive.ListFile(query).GetList()
    return file_list

def get_dir_reference(dir_path):
    ...

def up_files(file_paths, dir_path):
    ...

def check_files_exist(file_paths, dir_path):
    ...
