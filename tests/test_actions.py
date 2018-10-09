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
                
    @classmethod
    def setUpClass(cls):
        WinActions.StartApplication(r"C:\Windows\System32\notepad.exe")
        WinWait.TimeSleep(2)
                
    @classmethod
    def tearDownClass(cls):
        WinElement.SwitchToRootControl()
        WinElement.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)    
        WinActions.CloseWin()
    
    def test_WinElement(self):                
        WinElement.SwitchToRootControl()
        handles = WinElement._get_handles()
        self.assertEqual(len(handles),2)
        
        WinElement.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)
        prop = WinElement._get_search_property()        
        self.assertEqual(prop,{"ControlType":"WindowControl", "ClassName":"Notepad", "Depth":1, "index":1,"timeout":10})
        
        WinElement.SwitchToCurrentControl()
        handles = WinElement._get_handles()
        self.assertEqual(len(handles),3)
        
    def test_WinContext(self):
        WinElement.SwitchToRootControl()
        
        WinContext.SetVar("a","hello")
        self.assertEqual(WinContext.GetVar("a"), "hello")        
        
        WinElement.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)        
        WinElement.SwitchToCurrentControl()
                
        WinContext.DyPropertyData("class_name", "ClassName")
        self.assertEqual(WinContext.GetVar("class_name"), "Notepad")   
        
        WinElement.SetSearchProperty(ControlType = "EditControl", ClassName = "Edit")
        WinContext.DyTextData("text", re.compile('.*'))
        self.assertEqual(WinContext.GetVar("text"), "")
        
    def test_WinWait(self):
        WinElement.SwitchToRootControl()
        WinElement.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)
        
        self.assertTrue(WinWait.WaitForExist(timeout=2))
        WinWait.TimeSleep(2)
        self.assertFalse(WinWait.WaitForDisappear(timeout=2))
    
    def test_WinVerify(self):
        WinElement.SwitchToRootControl()
        WinElement.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)
        
        WinContext.SetVar("a","hello")
        self.assertTrue(WinVerify.VerifyVar("a", "hello"))
        
        self.assertTrue(WinVerify.VerifyExist())
        self.assertFalse(WinVerify.VerifyNotExist())
        self.assertTrue(WinVerify.VerifyElemEnabled())
        self.assertTrue(WinVerify.VerifyProperty("ClassName","Notepad"))
        self.assertTrue(WinVerify.VerifyProperty("Name", u"无标题 - 记事本"))
        self.assertTrue(WinVerify.VerifyKeyboardFocusable())
        self.assertFalse(WinVerify.VerifyKeyboardFocused())
                
    def test_WinActions(self):
        
        ### WindowPattern
        WinElement.SwitchToRootControl()
        WinElement.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)
        WinActions.ActivateWindow()
        WinActions.SetWinStat("maximize")
        WinActions.SetWinStat("normal")
        WinActions.SetTopmost(True)        
        WinActions.MoveWindowPos(400, 400)
        WinActions.MoveWindowPos()
        
        ### ValuePattern
        WinElement.SwitchToCurrentControl()
        WinElement.SetSearchProperty(ControlType = "EditControl", ClassName = "Edit")        
        WinActions.SetValue('Hello')
        self.assertEqual(WinActions.CurrentValue(), "Hello")
        
        #### Win32API to element
        WinActions.SendKeys('{Ctrl}{End}{Enter}World')
                        
        WinElement.SwitchToRootControl()
        WinElement.SetSearchProperty(ControlType = "WindowControl", ClassName = 'Notepad', Depth = 1)        
        WinActions.CloseWin()
        
        WinElement.SwitchToCurrentControl()        
        WinElement.SetSearchProperty(Name = u'保存(S)', ClassName = "CCPushButton")
        WinActions.Click(simulateMove = True)
        
        ### InvokePattern
        WinElement.SetSearchProperty(ControlType = "EditControl", Name = u'文件名:',ClassName="Edit", AutomationId = "1001")
        WinActions.SetValue(r'c:\some test dir')
        WinElement.SetSearchProperty(ControlType = "ButtonControl", Name = u'取消',ClassName="Button")
        WinActions.Invoke()
        
        WinElement.SetSearchProperty(ControlType = "EditControl", ClassName = "Edit")        
        WinActions.SetValue('')
    
        
        
if __name__ == "__main__":    
    unittest.main(verbosity=2)
#     suite = unittest.TestSuite()
#     suite.addTest(TestActions("test_WinVerify"))
#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(suite)
     