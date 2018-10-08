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


# __requires__ = 'uiautomation==1.1.10'
# __import__('pkg_resources').run_script('uiautomation==1.1.10', 'automation.py')


# import pkg_resources
# pkg_resources.run_script("uiautomation==1.1.10", "automation.py")


class T:
    #__t=123
    
    @classmethod
    def set(cls,v):
        cls.__t = v
        
    @classmethod
    def get(cls):
        return cls.__t
    
    
class Y(T):
    
    @classmethod
    def test(cls):
        print(cls.get())
        
if __name__ == "__main__":
    T.set(456)
    Y.test()
        
    