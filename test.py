# encoding: utf-8

import subprocess
import uiautomation as automation
 
def usage():
    print(automation.GetRootControl())
    subprocess.Popen('notepad.exe')
    notepadWindow = automation.WindowControl(searchDepth = 1, ClassName = 'Notepad')
    print(notepadWindow.Name)
    notepadWindow.SetTopmost(True)
    edit = notepadWindow.EditControl()
    edit.SetValue('Hello')
    edit.SendKeys('{Ctrl}{End}{Enter}World')
    notepadWindow.Close()
    notepadWindow.ButtonControl(Name=u'保存(S)').Invoke()
    notepadWindow.EditControl(Name="文件名:",AutomationId="1001").SetValue(r'c:\test dir')
    notepadWindow.ButtonControl(Name="取消").Invoke()
    notepadWindow.Close()
    notepadWindow.ButtonControl(Name=u'不保存(N)').Invoke()
    


# __requires__ = 'uiautomation==1.1.10'
# __import__('pkg_resources').run_script('uiautomation==1.1.10', 'automation.py')


# import pkg_resources
# pkg_resources.run_script("uiautomation==1.1.10", "automation.py")

        
if __name__ == "__main__":
    usage()
        
    