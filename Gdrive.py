#!/usr/bin/python3
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
class Drive:
    SERVICE=None
    SCOPES=None
    KEY_FILE_LOCATION=None
    FOLDER={"backups":"1u0mS3jdW6n3RifrO_0dFw7b8pkNVkFSl"}
    def __init__(self,scopes = ['https://www.googleapis.com/auth/drive.readonly'] ,key_file_location='./credentials.json'):
        self.SCOPES=scopes
        self.KEY_FILE_LOCATION=key_file_location
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_file_location, scopes)
        service = build('drive', 'v3', credentials=creds)
        self.SERVICE=service
    def ShowAllFolder(self):
        folder_id=self.FOLDER['backups']
        service=self.SERVICE        
        files = service.files().list(q=f"'{folder_id}' in parents").execute()
        for _file in files["files"]:
            print(_file["name"])
    def UploadFile(self):
        return
    def DownloadAll(self):
        return
           

drive=Drive()
drive.ShowAllFolder()      



