#! python3
# -*- encoding: utf-8 -*-
'''
Current module: wpfuidriver.actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      wpfuidriver.actions,  v1.0 2018年9月28日
    FROM:   2018年9月28日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import os,time,subprocess
import uiautomation

class WinUI(object):
    '''
    :prop dict properties of windows UI. 
        e.g.
            ControlType: str or unicode
            ClassName: str or unicode
            AutomationId: str or unicode
            Name: str or unicode
            SubName: str or unicode
            RegexName: str or unicode, supports regex
            Depth: integer, exact depth from searchFromControl, if set, searchDepth will be set to Depth too
    '''
    (prop,index,timeout)=({},1,10)
    
    __glob = {}
        
    #Context ----
    @classmethod
    def SetVar(cls, name, value):
        ''' set static value
        :param name: glob parameter name
        :param value: parameter value
        '''
        cls.__glob.update({name:value})
                
    @classmethod
    def GetVar(cls, name):
        return cls.__glob.get(name)
    
        
    #Verify ----
    @classmethod
    def VerifyKeyboardFocusable(cls):
        try:
            result = cls._element().IsKeyboardFocusable()
        except:
            result = False
        return result
    
    @classmethod
    def VerifyElemKeyboardFocus(cls):
        if cls.elm: 
            return cls.elm.getProp("HasKeyboardFocus")
        
    @classmethod
    def VerifyElemEnabled(cls):
        try:
            result = cls._element().IsEnabled()                          
        except:
            result = False
        return result
    
    @classmethod
    def VerifyClassName(cls, name):
        try:
            result = cls._element().ClassName == name
        except:
            result = False
        return result
        
    @classmethod
    def VerifyControlType(cls, contype):
        try:
            result = cls._element().ControlType == contype
        except:
            result = False
        return result
    
    @classmethod
    def VerifyAutomationId(cls, aid):
        try:
            result = cls._element().AutomationId == aid
        except:
            result = False
        return result    
    
    @classmethod
    def VerifyLocalizedControlType(cls, lct):
        try:
            result = cls._element().LocalizedControlType == lct
        except:
            result = False
        return result
        
    @classmethod
    def VerifyName(cls, name):
        try:
            result = cls._element().Name == name
        except:
            result = False
        return result
            
    @classmethod
    def BoundingRectangle(cls):
        if cls.elm: 
            return cls.elm.getProp("BoundingRectangle")    
    
    @classmethod
    def VerifyExist(cls):
        try:
            result = True if cls._element() else False
        except:
            result = False
        return result
        
    @classmethod
    def VerifyNotExist(cls):
        try:
            result = False if cls._element() else True
        except:
            result = True
        return result
    
    
    #Actions ---        
    @classmethod
    def TimeSleep(cls,seconds):
        time.sleep(seconds)
    
    @classmethod
    def StartApplication(cls, app_path):
        if not os.path.exists(app_path):
            raise Exception('Not found "%s"' %app_path)
        subprocess.Popen([app_path])
        
    ### InvokePattern
    @classmethod
    def Invoke(cls):
        ''' invoke element, just like click the element '''
        elm = cls._element()  
        try:
            if elm.IsInvokePatternAvailable():            
                elm.Invoke()
            else:
                return False
        except:
            return False
        
    ### ValuePattern
    @classmethod
    def SetValue(cls,value):
        ''' Set text value, just like type in some string '''
        elm = cls._element()  
        try:
            if elm.IsValuePatternAvailable():            
                elm.SetValue(value)
            else:
                return False
        except:
            return False
        
    ### ScrollPattern
    @classmethod
    def ScrollTo(cls,horizontalPercent=-1,verticalPercent=-1):
        ''' 
        :param horizontalPercent=-1 表示纵向滚动条; verticalPercent=100，表示向下移动100%,即移动到底; verticalPercent=0，表示顶端
        :param verticalPercent=-1 表示横向滚动条; horizontalPercent=100，表示向右移动100%,即移动到最右; horizontalPercent=0，表示左侧       
        '''
        
        elm = cls._element()  
        try:
            if elm.IsScrollPatternAvailable():
                elm.SetScrollPercent(horizontalPercent, verticalPercent)
            else:
                return False
        except:
            return False
        
        
    ### WindowPattern
    @classmethod
    def SetWinStat(cls,value):       
        
        stat = ["Normal", "Max", "Min"]
        if not value.capitalize() in stat:
            raise ValueError("SetWinStat need [Normal,Max,Min].")
        
        elm = cls._element()
        try:
            if elm.IsWindowPatternAvailable():
                getattr(elm, value.capitalize())()
            else:
                return False
        except:
            return False
                   
    
    @classmethod
    def CloseWin(cls):
        elm = cls._element()
        try:
            if elm.IsWindowPatternAvailable():
                elm.Close()
            else:
                return False
        except:
            return False
    
    ### TogglePattern        
    @classmethod
    def CheckOn(cls):
        '''
        :CheckBox 复选框 --可以多选, 如在方框中打勾，或填充 圆点
        :state 
            #    Indeterminate = 2
            #    On = 1
            #    Off = 0
        '''
        elm = cls._element()
        try:
            if elm.IsTogglePatternAvailable() and elm.CurrentToggleState == uiautomation.ToggleState.Off:
                elm.Toggle()
            else:
                return False
        except:
            return False
        
    @classmethod
    def CheckOff(cls):
        elm = cls._element()
        try:
            if elm.IsTogglePatternAvailable() and elm.CurrentToggleState == uiautomation.ToggleState.On:
                elm.Toggle()
            else:
                return False
        except:
            return False
    
    ### ExpandCollapsePattern          
    @classmethod
    def ExpandOn(cls):
        '''
        :ComboBox 组合框--->需要 下拉框选择的控件
        :state 有四种状态 
            #    LeafNode    =3
            #    PartiallyExpanded = 2
            #    Expanded = 1
            #    Collapsed = 0 
        '''
        elm = cls._element()
        try:
            if elm.IsExpandCollapsePatternAvailable() and elm.CurrentExpandCollapseState == uiautomation.ExpandCollapseState.Collapsed:
                elm.Expand()
            else:
                return False
        except:
            return False        
    
    @classmethod
    def ExpandOff(cls):
        elm = cls._element()
        try:
            if elm.IsExpandCollapsePatternAvailable() and elm.CurrentExpandCollapseState == uiautomation.ExpandCollapseState.Expanded:
                elm.Collapse()
            else:
                return False
        except:
            return False
        
    
    ### SelectionItemPattern
    @classmethod
    def SelectItem(cls):
        '''
        :ComboBox_ListBox 组合框 或者 列表框，展开后，选择条目
        :TabItem 选项卡项  ,选择条目
        '''
        elm = cls._element()
        try:
            if elm.IsSelectionItemPatternAvailable():
                elm.Select()
            else:
                return False
        except:
            return False
        
    
    #### Win32API to element
    @classmethod
    def Click(cls, ratioX = 0.5, ratioY = 0.5, simulateMove = True):
        """ 
        Click(0.5, 0.5): click center
        Click(10, 10): click left+10, top+10
        Click(-10, -10): click right-10, bottom-10
        simulateMove: bool, if True, first move cursor to control smoothly
        """
        elm = cls._element()
        try:
            elm.Click(ratioX = ratioX, ratioY = ratioY, simulateMove = simulateMove)
        except:
            return False
    
    @classmethod
    def DoubleClick(cls, ratioX = 0.5, ratioY = 0.5, simulateMove = True):
        ''' double click the element or positon
        DoubleClick(0.5, 0.5): double click center
        DoubleClick(10, 10): double click left+10, top+10
        DoubleClick(-10, -10): click right-10, bottom-10
        DoubleClick: bool, if True, first move cursor to control smoothly
        '''
        elm = cls._element()
        try:
            elm.DoubleClick(ratioX = ratioX, ratioY = ratioY, simulateMove = simulateMove)
        except:
            return False
    
    @classmethod
    def MouseDragDrop(cls):
        pass
    
    @classmethod
    def WheelDown(cls, times = 1):
        elm = cls._element()
        try:
            elm.WheelDown(times)
        except:
            return False
    
    @classmethod
    def MouseWheelUp(cls, times = 1):        
        elm = cls._element()
        try:
            elm.WheelUp(times)
        except:
            return False
    
    @classmethod
    def SendKeys(cls, text):
        """
        Simulate typing keys on keyboard
        keys: str, keys to type        
        example:
        {Ctrl}, {Delete} ... are special keys' name in Win32API.SpecialKeyDict
        SendKeys('{Ctrl}a{Delete}{Ctrl}v{Ctrl}s{Ctrl}{Shift}s{Win}e{PageDown}') #press Ctrl+a, Delete, Ctrl+v, Ctrl+s, Ctrl+Shift+s, Win+e, PageDown
        SendKeys('{Ctrl}(AB)({Shift}(123))') #press Ctrl+A+B, type (, press Shift+1+2+3, type ), if () follows a hold key, hold key won't release util )
        SendKeys('{Ctrl}{a 3}') #press Ctrl+a at the same time, release Ctrl+a, then type a 2 times
        SendKeys('{a 3}{B 5}') #type a 3 times, type B 5 times
        SendKeys('{{}Hello{}}abc {a}{b}{c} test{} 3}{!}{a} (){(}{)}') #type: {Hello}abc abc test}}}!a ()()
        SendKeys('0123456789{Enter}')
        SendKeys('ABCDEFGHIJKLMNOPQRSTUVWXYZ{Enter}')
        SendKeys('abcdefghijklmnopqrstuvwxyz{Enter}')
        SendKeys('`~!@#$%^&*()-_=+{Enter}')
        SendKeys('[]{{}{}}\\|;:\'\",<.>/?{Enter}')
        """
        elm = cls._element()
        try:
            elm.SendKeys(text)
        except:
            return False
    
    ####  Elemeent
    @classmethod
    def _element(cls):
        _prop = cls.prop.copy()
        control_str = _prop.pop("ControlType", "Control")
        if control_str in uiautomation.ControlTypeNameDict.values():
            control = getattr(uiautomation, "control_str")
        else:
            control = uiautomation.Control
        
        uiautomation.TIME_OUT_SECOND = cls.timeout
        _control = control(foundIndex = cls.index, **_prop)
        cls.index = 1
        return _control.Element

#     
def usage_for_mfc_app():    
    window_title1 = u"Installer Language"
    window_title2 = u"Notepad++ v5.7 安装" 
    WPFElement.StartApplication(r"F:\BaiduYunDownload\pcinstall\npp.5.7.Installer.exe")
    
    # Use UISpy or others to spy the WPF UI.    
    handle1 = WPFElement.SwitchToWindow(window_title1)
    print "handle1 ->", handle1  
    
    dpos = (400,400)
    WPFElement.identifications = {"AutomationId" : u"TitleBar"}
    WPFElement.MouseDragTo(*dpos)
    time.sleep(1)
    
    WPFElement.identifications = {"Name" : u"English"}
    WPFElement.SelectItem()
    
    WPFElement.identifications = {"Name" : u"Chinese (Simplified)"}
    WPFElement.SelectItem()
    
    WPFElement.identifications = {"Name" : u"OK"}  
    WPFElement.ClickWin()  
    print "---"
    
    handle2 = WPFElement.SwitchToWindow(window_title2)
    print "handle2 ->", handle2
    WPFElement.identifications = {"Name" : u"下一步(N) >"}
    WPFElement.ClickWin()
    
    WPFElement.identifications = {"Name" : u"我接受(I)"}
    WPFElement.ClickWin()
    
    WPFElement.identifications = {"AutomationId" : "1019"}
    WPFElement.TypeInWin(ur'd:\hello input你好')
    
    WPFElement.identifications = {"Name" : u"下一步(N) >"}
    WPFElement.ClickWin()
    
    WPFElement.identifications = {"Name" : u"取消(C)"}
    WPFElement.ClickWin()
    print "---"
    
    WPFElement.SwitchToDefaultWindow()
    WPFElement.identifications = {"Name" :  u"是(Y)"}
#     WPFElement.ClickWin()
    WPFElement.MouseClick()
    
def usage_for_wpf_app():
    dut = r"D:\auto\buffer\AiSchool\AiTeacherCenter\AiTeacherCenter\AiTeacher.exe"
    WPFElement.StartApplication(dut)
    
    #(identifications,prop,index,timeout)=({},None,0,10)
    WPFElement.identifications = {"AutomationId" : "txtUserName"}
    print "IsPassword: %s" %WPFElement.IsPassword()
    print "setting username value: Hello MUIA."
    WPFElement.TypeInWin("Hello MUIA")                
    print "---"
    
    WPFElement.identifications = {"AutomationId" : "PwdUser"}
    print "IsPassword: %s" %WPFElement.IsPassword()
    print "setting username value: 123456."
    WPFElement.TypeInWin("123456")                
    print "---"
        
    WPFElement.identifications = {"AutomationId" : "ckbIsSavePwd"}
    print "Name: %s" %WPFElement.Name()
    WPFElement.SwitchToggle()                    
    print "---"
    
    WPFElement.identifications = {"AutomationId" : "BtnLogin"}
    print "Name: %s" %WPFElement.Name()
    print "IsKeyboardFocusable: %s" %WPFElement.IsKeyboardFocusable()        
    WPFElement.ClickWin()
        
if __name__ == "__main__":    
    #ipy.exe driver.py
    ##### notepad++ installation example
    usage_for_mfc_app()
  
    #### AiSchool login example
#     usage_for_wpf_app()
    