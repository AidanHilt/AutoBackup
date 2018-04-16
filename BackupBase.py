import shutil
import logging
import sys
import pickle
import os
import time
from datetime import datetime
import DriveUpload as DU

FORMAT = "zip"

logging.basicConfig(format = "%(message)s",
                stream = sys.stdout,
                level = logging.DEBUG)
compressionLogger = logging.getLogger("pymotw")

"""Backup a file, with respect to last modified time (if modified over 30 minutes ago, it will not create a new backup)"""
def backupFile(backupPath, destinationPath, name, copies = False, numCopies = 30):
    theTime = str(datetime.now())
    theTime = theTime.replace(" ", "@")
    theTime = theTime.replace(":", ".")
    theTime = theTime[0:19]
    try:
        mTime = os.path.getmtime(backupPath)
        if(time.time() - mTime <= 10800):
            print("Copying " + backupPath + " to " + destinationPath)
            print("---------------------------------------------------")
            
            if copies:
                name = destinationPath + name + theTime
                shutil.make_archive(name, FORMAT, root_dir = backupPath,
                                    logger = compressionLogger)
                
            else:
                name = destinationPath + name
                shutil.make_archive(name, FORMAT, root_dir = backupPath,
                                    logger = compressionLogger)

            if copies:
                files = []
                filesList = os.scandir(destinationPath)
                for f in filesList:
                    files.append(f.path)
                files.sort(key=lambda x: os.path.getmtime(x))
                if len(files) > numCopies:
                    for file in files[0: len(files) - numCopies]:
                        os.remove(file)
            
            print("Complete")
            print("---------------------------------------------------")
    except FileNotFoundError:
        print("The file was not found, meaning it likely does not exist.")
        
    return name + "." + FORMAT
        

"""Backup files in the properly formatted list of dictionaries, while respecting modified time"""
def backupFiles(list):
    for dictionary in list:
        returnVal = backupFile(dictionary["backupPath"], dictionary["destinationPath"], dictionary["name"], dictionary["copies"],
                   dictionary["numCopies"])
        
        if dictionary["cloudBackup"] != -1 and time.time() - dictionary["cloudBackup"] >= 86400:
            DU.uploadFile(returnVal)
            dictionary["cloudBackup"] = time.time()
        
        
"""Backup a file, regardless of when it was last modified"""        
def backupAllFile(backupPath, destinationPath, name, copies = False, numCopies = 30):
    theTime = str(datetime.now())
    theTime = theTime.replace(" ", "@")
    theTime = theTime.replace(":", ".")
    theTime = theTime[0:19]
    print("Copying " + backupPath + " to " + destinationPath)
    print("---------------------------------------------------")

    if copies:
        shutil.make_archive(destinationPath + name + theTime, FORMAT, backupPath, logger = compressionLogger)
        
    else:
        shutil.make_archive(destinationPath + name, FORMAT, backupPath,  logger = compressionLogger)

    if copies:
        files = []
        filesList = os.scandir(destinationPath)
        for f in filesList:
            files.append(f.path)
        files.sort(key=lambda x: os.path.getmtime(x))
        if len(files) > numCopies:
            for file in files[0: len(files) - numCopies]:
                os.remove(file)

    print("Complete")
    print("---------------------------------------------------")
    
 
"""Backup files in the properly formatted list of dictionaries, regardless of when they were last modified"""    
def backupAllFiles(list):
    for dictionary in list:
        backupAllFile(dictionary["backupPath"], dictionary["destinationPath"], dictionary["name"], dictionary["copies"],
        dictionary["numCopies"])