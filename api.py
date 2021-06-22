import pydrive2
import os

def list_dir(drive, dir_id):
    query = {
        'supportsAllDrives': True,
        'q': "'{}' in parents and trashed=false".format(dir_id)
    }
    file_list = drive.ListFile(query).GetList()
    return file_list

def get_dir_reference(dir_path):
    query = {
        'id': dir_id
    }
    d = drive.CreateFile(query)
    d.FetchMetadata(fetch_all=True)
    return d

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
    f.Upload()
    return f

def up_files(drive, file_paths, dir_id):
    for file_path in file_paths:
        up_file(drive, file_path, dir_id)

def check_files_exist(drive, file_paths, dir_id):
    ...

def up_folder(drive, folder_path, dir_id):
    folder = create_new_folder(drive, folder_path, dir_id)
    folder.FetchMetadata()
    print(folder)
    folder_id = folder.metadata['id']
    file_paths = os.listdir(folder_path)
    file_paths = [os.path.join(folder_path, file_path) for file_path in file_paths]
    up_files(drive, file_paths, folder_id)