# encoding: utf-8

import subprocess
import uiautomation as automation
 
print(automation.GetRootControl())
subprocess.Popen('notepad.exe')
notepadWindow = automation.WindowControl(searchDepth = 1, ClassName = 'Notepad')
print(notepadWindow.Name)
notepadWindow.SetTopmost(True)
edit = notepadWindow.EditControl()
edit.SetValue('Hello')
edit.SendKeys('{Ctrl}{End}{Enter}World')


# __requires__ = 'uiautomation==1.1.10'
# __import__('pkg_resources').run_script('uiautomation==1.1.10', 'automation.py')


import pkg_resources
pkg_resources.run_script("uiautomation==1.1.10", "automation.py")