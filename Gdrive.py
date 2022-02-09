#!/usr/bin/python3
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
import io
import os
class Drive:
    SERVICE=None
    SCOPES=[
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.appdata'
            ]
    KEY_FILE_LOCATION=None
    FOLDER={"backups":"1u0mS3jdW6n3RifrO_0dFw7b8pkNVkFSl"}
    def __init__(self,key_file_location='./credentials.json'):
        self.KEY_FILE_LOCATION=key_file_location
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_file_location,self.SCOPES)
        service = build('drive', 'v3', credentials=creds)
        self.SERVICE=service
    def ShowAllFolder(self):
        folder_id=self.FOLDER['backups']
        service=self.SERVICE        
        files = service.files().list(q=f"'{folder_id}' in parents").execute()
        for _file in files["files"]:
            print(_file["name"],_file["id"])
    def UploadFile(self,filename):
        service=self.SERVICE
        folder_id=self.FOLDER['backups']
        file_metadata = {
            'name': filename,
            'parents': [folder_id],
            'mimeType': '*/*'
        }
        media = MediaFileUpload(filename,mimetype='*/*',resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print ('File ID: ' + file.get('id'))

        return
    def DownloadFile(self,file_id,filename):
        service=self.SERVICE
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb') 
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))           
    def DownloadAll(self):
        folder_id=self.FOLDER['backups']
        service=self.SERVICE        
        files = service.files().list(q=f"'{folder_id}' in parents").execute()
        for _file in files["files"]:
            file_id=_file["id"]
            filename=_file["name"]
            self.DownloadFile(file_id,filename)
            os.system(f"mv './{filename}' ./sql/")