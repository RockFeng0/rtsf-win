#! python3
# -*- encoding: utf-8 -*-
'''
Current module: winuidriver.actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      winuidriver.actions,  v1.0 2018年9月30日
    FROM:   2018年9月30日
********************************************************************
======================================================================

Provide a function for the automation test

'''


import os,time,subprocess,re
import uiautomation

class WinElement(object):
    
    __prop, __elm = {}, None
    
    __root = uiautomation.GetRootControl()
    __handles = [(__root.Handle, __root.Name)]
                    
    @classmethod    
    def SetSearchProperty(cls,**kwargs):
        '''
        @param kwargs:  dict properties of windows UI. 
            e.g.
                ControlType: str or unicode, always suggest to use, because some ControlType has special pattern functions
                ClassName: str or unicode
                AutomationId: str or unicode
                Name: str or unicode
                SubName: str or unicode
                RegexName: str or unicode, supports regex
                Depth: integer, exact depth from searchFromControl, if set, searchDepth will be set to Depth too
        '''
        cls.__elm = None
        cls.__prop = {"index":1, "timeout":10}        
        cls.__prop.update(kwargs)
    
    @classmethod
    def GetSearchProperty(cls):
        return cls.__prop
        
    @classmethod
    def SwitchToCurrentControl(cls):
        ''' switch to the child control '''        
        cls.__root = uiautomation.ControlFromHandle(cls.__handles[-1][0])        
        
    @classmethod
    def SwitchToRootControl(cls):
        ''' switch to root control '''
        cls.__root = uiautomation.GetRootControl()
    
    @classmethod
    def _element(cls):
        if cls.__elm:
            return cls.__elm
        
        _prop = cls.__prop.copy()        
        control_type = _prop.pop("ControlType", "Control")
        time_out = _prop.pop("timeout")
        
        if control_type in uiautomation.ControlTypeNameDict.values():        
            cls.__elm = control = getattr(cls.__root, control_type)(foundIndex = _prop.pop("index"), **_prop)
        else:
            cls.__elm = control = cls.__root.Control(foundIndex = _prop.pop("index"), **_prop)
        
        if not control._element: 
            control.Refind(maxSearchSeconds = time_out)
            
        handle = (control.Handle, control.Name)
        if handle in cls.__handles:
            cls.__handles.pop(cls.__handles.index(handle))
        cls.__handles.append(handle)                        
        return control

class WinContext(WinElement):
    
    glob = {}
      
    @classmethod
    def SetVar(cls, var, value):
        ''' set static value
        :param var: glob parameter name
        :param value: parameter value
        '''
        cls.glob.update({var:value})
                
    @classmethod
    def GetVar(cls, var):
        return cls.glob.get(var)     
    
    @classmethod
    def DyPropertyData(cls,var, attr):
        try:
            if attr in ('ClassName', 'ControlTypeName', 'Name', 'AutomationId'):
                result = getattr(cls._element(), attr)
            else:
                result = None
        except:
            result = None
        cls.SetVar(var, result)
        
    @classmethod
    def DyTextData(cls, var, regx, index = 0):
        ''' set dynamic value from the string data of response  
        @param var: glob parameter name
        @param regx: re._pattern_type
            e.g.
            DyStrData("a",re.compile('123'))
            
            CurrentValue
        '''
                
        if not isinstance(regx, re._pattern_type):
            raise Exception("DyTextData need the arg which have compiled the regular expression.")
        
        text = WinActions.CurrentValue()
        if text == False:
            result = ""
        else:    
            values = regx.findall(text)            
            result = ""
            if len(values)>index:
                result = values[index]
                    
        cls.glob.update({var:result})
           
    
class WinWait(WinElement):    
    
    @classmethod
    def TimeSleep(cls, seconds):
        time.sleep(seconds)
        
    @classmethod
    def WaitForExist(cls, timeout):
        return uiautomation.WaitForExist(cls._element(), timeout)
        
    @classmethod
    def WaitForDisappear(cls, timeout):
        return uiautomation.WaitForDisappear(cls._element(), timeout)
        
class WinVerify(WinElement):
    
    @classmethod
    def VerifyVar(cls, name, expect_value):
        return WinContext.GetVar(name) == expect_value
    
    @classmethod
    def VerifyProperty(cls, attr, expect_value):
        try:
            if attr in ('ClassName', 'ControlTypeName', 'Name', 'AutomationId'):
                result = getattr(cls._element(), attr) == expect_value
            else:
                result = False
        except:
            result = False
        finally:
            return result
    
    @classmethod
    def VerifyKeyboardFocusable(cls):
        try:
            result = cls._element().IsKeyboardFocusable()
        except:
            result = False
        return result
    
    @classmethod
    def VerifyElemKeyboardFocus(cls):
        try:
            result = cls._element().HasKeyboardFocus()                          
        except:
            result = False
        return result
        
    @classmethod
    def VerifyElemEnabled(cls):
        try:
            result = cls._element().IsEnabled()                          
        except:
            result = False
        return result
            
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
    
            
class WinActions(WinElement):
    @classmethod
    def StartApplication(cls, app_path):
        if not os.path.exists(app_path):
            raise Exception('Not found "%s"' %app_path)
        subprocess.Popen([app_path])
    
    ### WindowPattern
    @classmethod
    def SetWinStat(cls,value):       
        
        stat = ["Normal", "Max", "Min"]
        if not value.capitalize() in stat:
            raise ValueError("SetWinStat need [Normal,Max,Min].")
        
        elm = cls._element()        
        if elm.IsWindowPatternAvailable():
            getattr(elm, value.capitalize())()
        else:
            return False
                   
    @classmethod
    def ActivateWindow(cls):
        ''' activate and Move cursor to this window '''
        elm = cls._element()        
        if elm.IsWindowPatternAvailable():
            elm.SwitchToThisWindow()
        else:
            return False
    
    @classmethod
    def SetTopmost(cls, is_top_most = False):
        ''' 置顶    '''
        elm = cls._element()        
        if elm.IsWindowPatternAvailable():
            elm.SetTopmost(is_top_most)
        else:
            return False
        
    @classmethod
    def MoveWindowPos(cls,x=-1, y=-1):
        ''' defalut move window to center
        e.g.
            x = 400, y = 400
        '''
        elm = cls._element()        
        if x == -1 or y == -1:
            left, top, right, bottom = elm.BoundingRectangle
            width, height = right - left, bottom - top
            screenWidth, screenHeight = uiautomation.Win32API.GetScreenSize()
            x, y = (screenWidth-width)//2, (screenHeight-height)//2
            if x < 0: x = 0
            if y < 0: y = 0           
            
        return uiautomation.Win32API.SetWindowPos(elm.Handle, uiautomation.SWP.HWND_TOP, x, y, 0, 0, uiautomation.SWP.SWP_NOSIZE)
    
    @classmethod
    def CloseWin(cls):
        elm = cls._element()        
        if elm.IsWindowPatternAvailable():
            elm.Close()
        else:
            return False
        
    ### InvokePattern
    @classmethod
    def Invoke(cls):
        ''' invoke element, just like click the element '''
        elm = cls._element()
        if elm.IsInvokePatternAvailable():            
            elm.Invoke()
        else:
            return False
                
    ### ValuePattern
    @classmethod
    def SetValue(cls,value):
        ''' Set text value, just like type in some string '''
        elm = cls._element()
        if elm.IsValuePatternAvailable():            
            elm.SetValue(value)
        else:
            return False
        
    @classmethod
    def CurrentValue(cls):
        ''' Set text value, just like type in some string '''
        elm = cls._element()
        if elm.IsValuePatternAvailable():            
            return elm.CurrentValue()
        else:
            return False
        
    ### ScrollPattern
    @classmethod
    def ScrollTo(cls,horizontalPercent=-1,verticalPercent=-1):
        ''' 
        :param horizontalPercent=-1 表示纵向滚动条; verticalPercent=100，表示向下移动100%,即移动到底; verticalPercent=0，表示顶端
        :param verticalPercent=-1 表示横向滚动条; horizontalPercent=100，表示向右移动100%,即移动到最右; horizontalPercent=0，表示左侧       
        '''
        
        elm = cls._element()        
        if elm.IsScrollPatternAvailable():
            elm.SetScrollPercent(horizontalPercent, verticalPercent)
        else:
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
        if elm.IsTogglePatternAvailable() and elm.CurrentToggleState == uiautomation.ToggleState.Off:
            elm.Toggle()
        else:
            return False
                
    @classmethod
    def CheckOff(cls):
        elm = cls._element()        
        if elm.IsTogglePatternAvailable() and elm.CurrentToggleState == uiautomation.ToggleState.On:
            elm.Toggle()
        else:
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
        if elm.IsExpandCollapsePatternAvailable() and elm.CurrentExpandCollapseState == uiautomation.ExpandCollapseState.Collapsed:
            elm.Expand()
        else:
            return False        
    
    @classmethod
    def ExpandOff(cls):
        elm = cls._element()
        if elm.IsExpandCollapsePatternAvailable() and elm.CurrentExpandCollapseState == uiautomation.ExpandCollapseState.Expanded:
            elm.Collapse()
        else:
            return False        
    
    ### SelectionItemPattern
    @classmethod
    def SelectItem(cls):
        '''
        :ComboBox_ListBox 组合框 或者 列表框，展开后，选择条目
        :TabItem 选项卡项  ,选择条目
        '''
        elm = cls._element()
        if elm.IsSelectionItemPatternAvailable():
            elm.Select()
        else:
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
