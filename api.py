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

def create_empty_folder(drive, folder_title, dir_id):
    base_name = os.path.basename(folder_title)
    query = {
        'parents': [{'id':dir_id}],
        'title': base_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    f = drive.CreateFile(query)
    f.Upload()
    f.FetchMetadata()
    exist = check_files_exist(drive, [base_name], dir_id)[0]
    
    return f

def up_items(drive, file_paths, dir_id):
    items = []
    for file_path in file_paths:
        if os.path.isdir(file_path):
            f = create_empty_folder(drive, file_path, dir_id)
        else:
            f = up_file(drive, file_path, dir_id)
        items.append(f)
    return items

def check_files_exist(drive, file_paths, dir_id):
    query = {
        'supportsAllDrives': True,
        'q': "'{}' in parents and trashed=false".format(dir_id)
    }
    file_list = drive.ListFile(query).GetList()
    file_list_title = [f['title'] for f in file_list]
    return [True if file_path in file_list_title else False for file_path in file_paths]

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

def up_folder(drive, folder_path, dir_id, recursive=False):
    folder_basename = os.path.basename(folder_path)
    if check_files_exist(drive, [folder_basename], dir_id):
        print("Existing a folder with the same name")
        folder = get_reference_by_name(drive, folder_basename, dir_id)
    else:
        print("Creating a new folder")
        folder = create_empty_folder(drive, folder_basename, dir_id)
    folder_id = folder.metadata['id']

    if recursive:
        file_pathss = []
        folder_ids = []
        folder_paths = []
        
        folder_paths.append(folder_path)
        folder_ids.append(folder_id)
        while(True):

            current_folder_path = folder_paths[0]
            folder_paths = folder_paths[1:]
            current_folder_id = folder_ids[0]
            folder_ids = folder_ids[1:]

            current_item_paths = os.listdir(current_folder_path)
            current_item_paths = [os.path.join(current_folder_path, current_item_path) for current_item_path in current_item_paths]
            current_file_paths = [current_item_path for current_item_path in current_item_paths if not os.path.isdir(current_item_path)]
            current_folder_paths = [current_item_path for current_item_path in current_item_paths if os.path.isdir(current_item_path)]

            up_items(drive, current_file_paths, current_folder_id)

            if len(current_folder_paths) > 0:
                current_folder_instances = up_items(drive, current_folder_paths, current_folder_id)
                current_folder_ids = [instance.metadata['id'] for instance in current_folder_instances]
                folder_ids.extend(current_folder_ids)
                folder_paths.extend(current_folder_paths)
            if len(folder_ids) == 0:
                break
    else:
        file_paths = os.listdir(folder_path)
        file_paths = [os.path.join(folder_path, file_path) for file_path in file_paths]
        up_items(drive, file_paths, folder_id)