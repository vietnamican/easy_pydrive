import pydrive2
import os

def list_dir(drive, dir_id):
    query = {
        'supportsAllDrives': True,
        'q': "'{}' in parents and trashed=false".format(dir_id)
    }
    file_list = drive.ListFile(query).GetList()
    return file_list

def up_file(drive, file_path, dir_id, is_folder=False):
    base_name = os.path.basename(file_path)
    query = {
        'parents': [{'id':dir_id}],
        'title': base_name
    }
    f = drive.CreateFile(query)
    f.SetContentFile(file_path)
    f.Upload()
    return f

def create_new_folder(drive, folder_title, dir_id):
    query = {
        'parents': [{'id':dir_id}],
        'title': folder_title,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    f = drive.CreateFile(query)
    exist = check_files_exist(drive, [folder_title], dir_id)[0]
    if exist:
        print("Existing a folder with the same name")
        f = get_reference_by_name(drive, folder_title, dir_id)
    else:
        print("Creating a new folder")
        f.Upload()
        f.FetchMetadata()
    return f

def get_reference_by_name(drive, file_title, dir_id):
    exist = check_files_exist(drive, [file_title], dir_id)[0]
    if not exist:
        print("Not exist file for given name")
    else:
        query = {
            'supportsAllDrives': True,
            'q': "'{}' in parents and trashed=false".format(dir_id)
        }
        file_list = drive.ListFile(query).GetList()
        for f in file_list:
            if f['title'] == file_title:
                return f

def up_files(drive, file_paths, dir_id):
    for file_path in file_paths:
        up_file(drive, file_path, dir_id)

def check_files_exist(drive, file_paths, dir_id):
    query = {
        'supportsAllDrives': True,
        'q': "'{}' in parents and trashed=false".format(dir_id)
    }
    file_list = drive.ListFile(query).GetList()
    file_list_title = [f['title'] for f in file_list]
    return [True if file_path in file_list_title else False for file_path in file_paths]

def up_folder(drive, folder_path, dir_id):
    folder = create_new_folder(drive, folder_path, dir_id)
    # print(folder)
    folder_id = folder.metadata['id']
    file_paths = os.listdir(folder_path)
    file_paths = [os.path.join(folder_path, file_path) for file_path in file_paths]
    up_files(drive, file_paths, folder_id)