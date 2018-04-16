from tkinter import *
import tkinter as tk
import pickle
import winshell
import os
import ctypes, sys
import time

from win32com.client import Dispatch
from tkinter import filedialog
from test.test_decimal import file

settings = {}

try:
    with open("settings.txt", 'rb') as file:
        settings = pickle.load(file)
        INSTALL_PATH = settings["InstallPath"]
        print(INSTALL_PATH)
except:
    with open("settings.txt", 'wb+') as file:
        settings["InstallPath"] = os.getcwd()
        INSTALL_PATH = settings["InstallPath"]
        pickle.dump(settings, file)
    
SHORTCUT_PATH = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\AutoBackup.lnk"

"""List of dictionaries that are used for backupFiles() arguments"""

with open("backups.txt", 'rb') as file:
    dictList = pickle.load(file)

root = Tk()

root.geometry("800x400+100+100")

num = 0
copiesButtonVal = IntVar()
startupCheckboxVal = IntVar()
currentItemCloudBackup = IntVar()

"""-------------------------End of opening-----------------------------"""


"""Function definitions"""
def createShortcut():
    if startupCheckboxVal.get() == 1:
        targetPath = INSTALL_PATH  + "/AutoBackup.pyw"
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(SHORTCUT_PATH)
        shortcut.Targetpath = targetPath
        shortcut.IconLocation = targetPath
        shortcut.WorkingDirectory = INSTALL_PATH
        shortcut.save()
    else:
        os.remove(SHORTCUT_PATH)

def delete():
    global num
    del dictList[num]
    if num - 1 > 0:
        num -= 1
    else:
        num += 1
    updateListbox()
    onListSelection()

def save():
    global num
    dictList[num]["backupPath"] = backupPathTextDisplay.get(1.0, END)
    dictList[num]["backupPath"] = dictList[num]["backupPath"].replace("\n", "")
    dictList[num]["backupPath"] = dictList[num]["backupPath"].strip()
    dictList[num]["destinationPath"] = destinationPathTextDisplay.get(1.0, END)
    dictList[num]["destinationPath"] = dictList[num]["destinationPath"].replace("\n", "")
    dictList[num]["destinationPath"] = dictList[num]["destinationPath"].strip()
    dictList[num]["name"]=nameTextDisplay.get(1.0, END)
    dictList[num]["name"] = dictList[num]["name"].replace("\n", "")
    dictList[num]["name"] = dictList[num]["name"].strip()
    
    if currentItemCloudBackup.get() == 0:
        dictList[num]["cloudBackup"] = -1
    elif currentItemCloudBackup.get() == 1 and dictList[num]["cloudBackup"] == -1:
        dictList[num]["cloudBackup"] = time.time()

    if copiesButtonVal.get() == 0:
        dictList[num]["copies"] = False
    elif copiesButtonVal.get() == 1:
        dictList[num]["copies"] = True
        
    

    dictList[num]["numCopies"] = int(copiesNumberDisplay.get())

    with open("backups.txt", 'wb') as file:
        pickle.dump(dictList, file)
        
    updateListbox()
    
def changeCheckButton(change):
    if change:
        copiesCheckDisplay.select()
        copiesNumberDisplay.configure(state = tk.NORMAL)
    else:
        copiesCheckDisplay.deselect()
        copiesNumberDisplay.config(state = tk.DISABLED)

def updateFields(self):
    global num
    num = namesList.curselection()[0]
    onListSelection()

def onListSelection():
    global num
    setText(backupPathTextDisplay, dictList[num]["backupPath"])
    setText(destinationPathTextDisplay, dictList[num]["destinationPath"])
    setText(nameTextDisplay, dictList[num]["name"])
    copies = dictList[num]["copies"]
    if copies:
        changeCheckButton(copies)
        copiesNumberDisplay.delete(0, 15)
        copiesNumberDisplay.insert(INSERT, dictList[num]["numCopies"])
    else:
        copiesNumberDisplay.delete(0, 15)
        copiesNumberDisplay.insert(INSERT, dictList[num]["numCopies"])
        changeCheckButton(copies)
    
    
def setText(text, string):
    if string != "":
        text.delete(1.0, END)
        text.insert(INSERT, string)

def openBackedFileSelector():
    setText(backupPathTextDisplay, filedialog.askdirectory(title = "Select directory to back up"))

def openDestinationFileSelector():
    setText(destinationPathTextDisplay, filedialog.askdirectory(title = "Select destination for backup file"))

def updateListbox():
    namesList.delete(0, END)
    for dict in reversed(dictList):
        namesList.insert(0, dict["name"])
        
def modifyCopiesNum():
    if copiesButtonVal.get() == 0:
        copiesNumberDisplay.config(state = DISABLED)
    if copiesButtonVal.get() == 1:
        copiesNumberDisplay.config(state = NORMAL)
        
def addEntry():
    global num
    print("Engaged")
    dictList.append({"backupPath": "Enter path here", "destinationPath": "Enter path here", "name": "Enter name here" , "copies": False, "numCopies": 0})
    updateListbox()
    num = len(dictList) - 1
    onListSelection()
        
"""End of definitions"""    

"""Listbox with names of sets to back up"""
namesList = tk.Listbox(root, selectmode=tk.SINGLE)

updateListbox()
    
namesList.bind('<<ListboxSelect>>', updateFields)
namesList.grid(column = 0)

saveButton = tk.Button(root, activebackground = "#b3ecff", activeforeground = "#00ace6", anchor = tk.CENTER,
                       text = "Save", command = save)
saveButton.grid(column = 2, row = 6)

"""-----------End of listbox---------------"""

"""Backup Path Selection"""
backupPathSelectorButton = tk.Button(root, activebackground = "#b3ecff", activeforeground = "#00ace6", anchor = tk.CENTER,
                           text = "Select path", command = openBackedFileSelector)

backupPathSelectorButton.grid(column = 2, row = 0)



backupPathTextDisplay = tk.Text(root, height = 1, width = 72)
backupPathTextDisplay.insert(INSERT, dictList[num]["backupPath"])
backupPathTextDisplay.grid(column = 1, row = 0)
"""----------End of Backup Path Selection-----------"""

"""Destination Path Selection"""
destinationPathSelectorButton = tk.Button(root, activebackground = "#b3ecff", activeforeground = "#00ace6", anchor = tk.CENTER,
                                          text = "Select path", command = openDestinationFileSelector)
destinationPathSelectorButton.grid(column = 2, row = 1)

destinationPathTextDisplay = tk.Text(root, height = 1, width = 72)
destinationPathTextDisplay.insert(INSERT, dictList[num]["destinationPath"])
destinationPathTextDisplay.grid(column = 1, row = 1)
"""----------End of Destination Path Selection------------------"""

"""Text display for name"""
nameTextDisplay = tk.Text(root, height = 1, width = 72)
nameTextDisplay.insert(INSERT, dictList[num]["name"])
nameTextDisplay.grid(column = 1, row = 2)
"""------------ End of text display for name------------------"""


"""Number of copies"""
copiesNumberDisplay = tk.Spinbox(root, from_=1, to=30, width = 2)
copiesNumberDisplay.delete(0, END)
copiesNumberDisplay.insert(INSERT, dictList[num]["numCopies"])
copiesNumberDisplay.grid(column = 1, row = 4)
"""-------------End of number of copies----------------"""

"""Copies boolean"""
copiesCheckDisplay = tk.Checkbutton(root, activebackground = "#b3ecff", activeforeground = "#00ace6", text = "Copies", 
                                    variable = copiesButtonVal, command = modifyCopiesNum)
if dictList[num]["copies"]:
    copiesCheckDisplay.select()
    copiesNumberDisplay.config(state = NORMAL)
else:
    copiesCheckDisplay.deselect()
    copiesNumberDisplay.config(state = DISABLED)

copiesCheckDisplay.grid(column = 1, row = 3)
"""------------End of copies boolean---------------"""

"""Delete button"""
deleteButton = tk.Button(root, activebackground = "#b3ecff", activeforeground = "#00ace6", text = "Delete", command = delete)
deleteButton.grid(column = 2, row = 2)
""""------------End of delete button-------------------"""

addNewFileButton = tk.Button(root, activebackground = "#b3ecff", activeforeground = "#00ace6", anchor = tk.CENTER,
                             text = "+", command = addEntry)
addNewFileButton.grid(column = 0, row = 1)


"""Run on startup checkbox"""
startupCheckbox = tk.Checkbutton(root, activebackground = "#b3ecff", activeforeground = "#00ace6", text = "Run on startup",
                                command = createShortcut, variable = startupCheckboxVal)
if os.path.isfile(SHORTCUT_PATH):
    startupCheckbox.select()
    
startupCheckbox.grid(column = 0, row = 2)

"""Cloud backup checkbox"""
cloudBackupCheckbox = tk.Checkbutton(root, activebackground = "#b3ecff", activeforeground = "#00ace6", text = "Cloud Backup", variable = currentItemCloudBackup)
cloudBackupCheckbox.grid(column=0, row=3)

try:
    if dictList[num]["cloudBackup"]:
        cloudBackupCheckbox.select()
    else:
        cloudBackupCheckbox.deselect()
except:
    cloudBackupCheckbox.deselect()
        
root.mainloop()