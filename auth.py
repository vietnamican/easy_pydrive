from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

def get_drive_instance():
    gauth = GoogleAuth()
    gauth.CommandLineAuth()

    return GoogleDrive(gauth)