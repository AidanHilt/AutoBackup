import pickle
import BackupBase as bb

backups = {}
with open("backups.txt", 'rb') as file:
	backups = pickle.load(file)
	for item in backups:
		print(item["name"])
	
bb.backupAllFiles(backups)