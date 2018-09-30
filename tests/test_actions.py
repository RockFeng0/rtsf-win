#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_actions,  v1.0 2018年9月30日
    FROM:   2018年9月30日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest,re

from winuidriver.actions import WinActions,WinContext,WinElement,WinVerify,WinWait

class TestActions(unittest.TestCase):
    
    def setUp(self):
        self.program = r"C:\Windows\System32\notepad.exe"
    
    def test_usage(self):
        WinActions.StartApplication(self.program)
        WinWait.TimeSleep(2)
        
        WinActions.SwitchToRootControl()
        WinActions.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)
        WinActions.ActivateWindow()
        WinActions.MoveWindowPos(400, 400)    
        WinVerify.VerifyProperty("Name", u"无标题 - 记 事本")    
        WinWait.TimeSleep(2)
        
        WinActions.SwitchToCurrentControl()
        WinActions.SetSearchProperty(ControlType = "EditControl", ClassName = "Edit")
        WinContext.DyPropertyData("class_name", "ClassName")
        WinVerify.VerifyVar("class_name", "Edit")
        WinActions.SetValue('Hello')
        WinActions.SendKeys('{Ctrl}{End}{Enter}World')
        WinContext.DyTextData("text", re.compile('.*'))
        WinVerify.VerifyVar("text", "Helloss\r\nWorlda")
        WinWait.TimeSleep(2)
        
        WinActions.SwitchToRootControl()
        WinActions.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)
        WinActions.MoveWindowPos()
        WinWait.TimeSleep(2)
        WinActions.CloseWin()
        
        WinActions.SwitchToCurrentControl()
        WinActions.SetSearchProperty(Name = u'保存(S)', ClassName = "CCPushButton")
        WinActions.Click(simulateMove = True)
        WinActions.SetSearchProperty(ControlType = "EditControl", Name = u'文件名:',ClassName="Edit", AutomationId = "1001")
        WinActions.SetValue(r'c:\some test dir')
        WinActions.SetSearchProperty(ControlType = "ButtonControl", Name = u'取消',ClassName="Button")
        WinActions.Invoke()
        
        WinActions.SwitchToRootControl()
        WinActions.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)    
        WinActions.CloseWin()
        WinWait.TimeSleep(2)
        WinActions.SetSearchProperty(ControlType = "ButtonControl", Name = u'不保存(N)', ClassName = "CCPushButton")
        WinActions.Invoke()
    
        
        
if __name__ == "__main__":    
    unittest.main(verbosity=2)
    