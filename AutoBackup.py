import atexit
import BackupBase as bb
import pickle
import time
import os
import DriveUpload as du
with open("settings.txt", "rb") as file:
	settings = pickle.load(file)

with open("backups.txt", "rb") as file:
    list = pickle.load(file)

firstTime = time.time()
minuteTime = time.time()

def exitProgram():
    with open("settings.txt", "wb") as file:
        settings["closeTime"] = time.time()
        pickle.dump(settings, file)
    
      
print("-----------------------------------------------------------------")
print("                     STARTING NEW RUN"                            )
print("-----------------------------------------------------------------")
startTime = time.time()

atexit.register(exitProgram)

try:
    startEndDiff = startTime - settings["closeTime"]
except:
    settings["closeTime"] = 0
    startEndDiff = startTime

for dictionary in list:
    try:
        fileDiff = startTime - os.path.getmtime(dictionary["backupPath"])
        try:    
            if startEndDiff > fileDiff:
                bb.backupAllFile(dictionary["backupPath"], dictionary["destinationPath"], dictionary["name"], dictionary["copies"],
                       dictionary["numCopies"])
                print("Finished")
        except PermissionError:
            print("Backup operation failed.")
    except FileNotFoundError:
        print("Could not get file last modified time, file likely does not exist: " + dictionary["name"])          
        
while(True):
    if time.time() - firstTime >= 3600:
        firstTime = time.time()
        bb.backupFiles(list)
    else:
        time.sleep(60)
