import pydrive2
import os

SKIP_EXIST = 0
OVERRIDE = 1
KEEP_VERSIONS = 2

def get_basenames(paths):
    if isinstance(paths, list):
        return [os.path.basename(path) for path in paths]
    else:
        return os.path.basename(paths)

def get_filter(sequence, keeps):
    return [item for item, keep in zip(sequence, keeps) if keep]

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
    base_name = get_basenames(folder_title)
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
    file_basenames = get_basenames(file_paths)
    query = {
        'supportsAllDrives': True,
        'q': "'{}' in parents and trashed=false".format(dir_id)
    }
    file_list = drive.ListFile(query).GetList()
    file_list_title = [f['title'] for f in file_list]
    return [True if file_basename in file_list_title else False for file_basename in file_basenames]

def get_references_by_names(drive, file_titles, dir_id):
    file_basenames = get_basenames(file_titles)
    query = {
        'supportsAllDrives': True,
        'q': "'{}' in parents and trashed=false".format(dir_id)
    }
    items = []

    file_list = drive.ListFile(query).GetList()
    file_list_titles = [f['title'] for f in file_list]
    for file_basename in file_basenames:
        for i, f_title in enumerate(file_list_titles):
            if file_basename  == f_title:
                items.append(file_list[i])
                break
    return items

def delete_items(drive, file_paths, dir_id):
    file_basenames = get_basenames(file_paths)
    exists = check_files_exist(drive, file_paths, dir_id)
    file_basenames = get_filter(file_basenames, exists)
    file_instances = get_references_by_names(drive, file_paths, dir_id)
    for file_instance in file_instances:
        file_instance.Trash()

def up_folder(drive, folder_path, dir_id, up_mode = SKIP_EXIST, recursive=True):
    folder_basename = get_basenames(folder_path)
    if check_files_exist(drive, [folder_basename], dir_id)[0]:
        print("Existing a folder with the same name")
        folder = get_references_by_names(drive, [folder_basename], dir_id)[0]
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
            
            # start a iteration
            current_folder_path = folder_paths[0]
            folder_paths = folder_paths[1:]
            current_folder_id = folder_ids[0]
            folder_ids = folder_ids[1:]
            current_item_paths = os.listdir(current_folder_path)
            current_item_paths = [os.path.join(current_folder_path, current_item_path) for current_item_path in current_item_paths]

            # upload files
            current_file_paths = [current_item_path for current_item_path in current_item_paths if not os.path.isdir(current_item_path)]
            if up_mode == SKIP_EXIST:
                exist = check_files_exist(drive, current_file_paths, current_folder_id)
                # print(exist)
                current_file_paths = get_filter(current_file_paths, exist)
            elif up_mode == OVERRIDE:
                delete_items(drive, current_file_paths, current_folder_id)
            up_items(drive, current_file_paths, current_folder_id)

            # recursive for subfolder
            current_folder_paths = [current_item_path for current_item_path in current_item_paths if os.path.isdir(current_item_path)]
            if len(current_folder_paths) > 0:
                print(current_folder_paths)
                exist = check_files_exist(drive, current_folder_paths, current_folder_id)
                exist_folder_paths = get_filter(current_folder_paths, exist)
                print(exist_folder_paths)
                non_exist_folder_paths = [current_folder_paths[i] for i, status in enumerate(exist) if not status]

                # print(exist_folder_paths)
                exist_folder_instances = get_references_by_names(drive, exist_folder_paths, current_folder_id)
                non_exist_folder_instances = up_items(drive, non_exist_folder_paths, current_folder_id)
                
                current_folder_instances = exist_folder_instances + non_exist_folder_instances
                current_folder_ids = [instance.metadata['id'] for instance in current_folder_instances]

                folder_ids.extend(current_folder_ids)
                folder_paths.extend(current_folder_paths)

            # stop the algorithm
            if len(folder_ids) == 0:
                break
    else:
        file_paths = os.listdir(folder_path)
        file_paths = [os.path.join(folder_path, file_path) for file_path in file_paths]
        up_items(drive, file_paths, folder_id)