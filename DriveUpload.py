import httplib2
import os

from apiclient.http import MediaFileUpload
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPE = "https://www.googleapis.com/auth/drive.file"
CLIENT_SECRET = "client_secret.json"
APP_NAME = "AutoBackup"

def getCredentials():
    homeDirectory = os.path.expanduser("~")
    credentialDirectory = os.path.join(homeDirectory, ".credentials")
    if not os.path.exists(credentialDirectory):
        os.makedirs(credentialDirectory)
    credentialPath = os.path.join(credentialDirectory, "AutoBackup.json")
    
    credentialStorage = Storage(credentialPath)
    credentials = credentialStorage.get()
    
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPE)
        flow.user_agent = APP_NAME
        
        print("Getting authorization")
        
        if flags:
            credentials = tools.run_flow(flow, credentialStorage, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        
        print("Storing credentials")
    
    return credentials
    
def uploadFile(path):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("drive", "v3", http=http)
    
    
    metadata = {"name": os.path.basename(path)}
    folder = MediaFileUpload(path, resumable = True)
    backupCopy = service.files().create(body = metadata, media_body=folder).execute()
    
def deleteFile(file):
    credentials = getCredentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build("drive", "v3", http=http)
    
    idList = service.files().list(q="name=" + "\'" + file + "\'").execute()
    fileId = idList["files"][0]["id"]
    service.files().delete(fileId=fileId).execute()
