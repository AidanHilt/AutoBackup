import ctypes, sys, os

ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "AutoBackupGUI.py", None, 1)