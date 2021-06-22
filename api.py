import pydrive2

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

def up_file(drive, file_path, dir_id):
    query = {
        'parents': [{'id':dir_id}]
    }
    f = drive.CreateFile(query)
    f.SetContentFile('README.md')
    f.Upload()


def up_files(drive, file_paths, dir_id):
    for file_path in file_paths:
        up_file(drive, file_path, dir_id)

def check_files_exist(drive, file_paths, dir_id):
    ...
