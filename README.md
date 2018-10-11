# rtsf-win
基于rtsf测试框架，关键字驱动Windows UI层面，进行自动化的控制及功能测试


## 环境准备

pip install rtsf-win


## 编写测试用例，模板基于rtsf

> 变量引用-> $var    关键字(函数)引用-> ${function}

- 常量的定义， glob_var 和  glob_regx
- 模板常用的关键字，参见 [rtsf](https://github.com/RockFeng0/rtsf)介绍

### 如何获取控件

运行 automation.py -h

![uiautomation-h.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-win-img/uiautomation-h.png)

automation中的参数示例如下:

automation.py -r -d 1 -t 0 ,# print desktop(the root of control tree) and it's children(top level windows) 
automation.py -t 0 -n -m ,# print current active window's controls, show fullname, show more properties
automation.py -t 3 ,# 延时3秒，打印当前激活窗口的树形结构，默认深度为1; 比如，此时打开notepad.exe,等待一会，automation.py会打印Notepad的所有控件树，并保存在 @AutomationLog.txt

```
# 一个简单的示例
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
notepadWindow.Close()
notepadWindow.ButtonControl(Name=u'保存(S)').Invoke()
notepadWindow.EditControl(Name="文件名:",AutomationId="1001").SetValue(r'c:\test dir')
notepadWindow.ButtonControl(Name="取消").Invoke()
notepadWindow.Close()
notepadWindow.ButtonControl(Name=u'不保存(N)').Invoke()
```

另外一个 UI工具, [Inspect.exe](https://docs.microsoft.com/zh-cn/windows/desktop/WinAuto/inspect-objects) 由 Microsoft支持,也能遍历windows UI元素. 不同的是，该工具有界面，而automation是个终端输出.不过，习惯了automation，你会发现更方便

![inspect-exe.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-win-img/inspect-exe.png)

[详细介绍](http://www.cnblogs.com/Yinkaisheng/p/3444132.html)


### 基本用例

基本用例，是指没有分层的情况下，简单的测试用例

```
# test_case.yaml
# yaml测试用例，模型示例:
- project:
    name: xxx Window
    module: xxx模块-功能测试
    
- case:
    # id 必填
    id: ATP-1
    # desc 必填
    desc: 测试用例-模板格式的设计-模板（全字段）
    
    # responsible 选填
    responsible: rockfeng0
    
    # tester 选填
    tester: rockfeng0
    
    # 定义正则表达式, 定义的字符串不会解析,选填
    glob_regx:
        rex_open_file: '(文件名.*)'
        rex_hello: 'Hello'
    
    # 定义变量， 效果同 SetVar(name, value),选填
    glob_var:
        program: C:\Windows\System32\notepad.exe
        title: 无标题 - 记事本
        keys: '{Ctrl}{End}{Enter}World'
        text_hello: 'Hello'
        text_save: '保存(S)'
        text_file_path: 'c:\some test dir'
        text_unsave: '不保存(N)'
        
    # pre_command 选填
    pre_command:
        - ${StartApplication($program)}
        - ${TimeSleep(2)}
        - ${SwitchToRootControl()}
        
    # steps 必填
    steps:      
    
        # 在windows中，定位元素            
        - windriver:
            ControlType: WindowControl
            ClassName: Notepad
            Depth: 1
            index: 1
            timeout: 10
            action: ${ActivateWindow()}
            
        - windriver:
            action: ${MoveWindowPos(400, 400)}
            
        - windriver:
            action: ${VerifyProperty(Name, $title)}
        
        - windriver:
            action: ${TimeSleep(2)} 
            
        - windriver:
            action: ${SwitchToCurrentControl()}
                    
        - windriver:
            action: ${SetSearchProperty(ControlType=EditControl, ClassName=Edit)}
            
        - windriver:
            action: ${DyPropertyData(class_name, ClassName)}
        
        - windriver:
            action: ${VerifyVar(class_name, Edit)} 
        
        - windriver:
            action: ${SetValue(Hello)}
                
        - windriver:          
            action: ${SendKeys($keys)}
                           
    # post_command 选填
    post_command:
        - ${DyTextData(text, $rex_hello)}
    
    # verify 选填
    verify:
        - ${VerifyVar(text, $text_hello)} 

```

### 分层用例

- 分层用例，是指模块功能测试的时候，对测试用例进行分层，最小的单元为api，其次为suite，最后组成用例
- 其存放路径、编写规则等，详见 [rtsf](https://github.com/RockFeng0/rtsf)相关介绍
- 示例可以，参见[rtsf-http](https://github.com/RockFeng0/rtsf-http)相关介绍


## 执行测试用例

### windriver 命令

```
# 查看帮助 -h 
windriver -h

# 执行测试用例
windriver C:\f_disk\BaiduNetdiskDownload\rtsf-win\tests\data\test_case.yaml
```

## 测试报告及日志

> 执行结束后，测试用例所在路径，就是report生成的路径


to do-------------------------

## 封装的关键字(内置函数)

关键字的使用，在前面，有介绍，规则如下
> 变量引用-> $var    关键字(函数)引用-> ${function}

### 浏览器相关操作

Web functions | 参数介绍 | 描述
--------------|----------|-----
AlertAccept()        | |点击alert弹窗的Accept(确定)
AlertDismiss()       | |点击alert弹窗的Dismiss(取消)
AlertSendKeys(value) | |向alert弹窗中输入信息
Back()               | |浏览器后退
Forward()            | |浏览器前进
IESkipCertError()    | |IE Skip SSL Cert Error
Js(script)           | |浏览器执行js脚本
Maximize()           | |浏览器最大化
NavigateTo(url)      | |浏览器打开url
NewTab()             | |浏览器新开标签页，并将所有焦点指向该标签页
PageSource()         | |当前页面源码
Refresh()            | |浏览器刷新当前页面
ScreenShoot(pic_path)| |截图当前页面，并为pic_path
ScrollTo(x,y)        | |移动滚动条至(x,y),如下，X-Y-top :  ScrollTo("0","0"); X-bottom:  ScrollTo("10000","0");Y-bottom:  ScrollTo("0","10000")
SetWindowSize(width, height)| |设置浏览器窗口大小
SwitchToAlert()             | |切换浏览器焦点至alert弹窗
SwitchToDefaultFrame()      | |切换浏览器焦点至默认frame框, 比如打开的页面有多个iframe的情况
SwitchToDefaultWindow()     | |切换浏览器焦点至默认window窗,比如多个标签页窗的情况
SwitchToNewFrame(frame_name)| |切换浏览器焦点至frame_name框
SwitchToNewWindow()         | |切换浏览器焦点至新window窗
WebClose()                  | |关闭浏览器当前窗口
WebQuit()                   | |Quits the driver and closes every associated window.

###  元素定位相关操作

<table>
    <tr>
        <th>WebElement methods</th>
        <th>参数介绍</th>
        <th>描述</th>
    </tr>
    <tr>
        <td>GetControl()</td>
        <td> </td>
        <td>获取element controls,返回字典，如：{"by":None,"value":None,"index":0,"timeout":10}</td>
    </tr>
    <tr>
        <td rowspan="4">SetControl(by,value,index,timeout)</td>
        <td>by: 指selenium的寻找元素的方式("id", "xpath", "link text","partial link text","name", "tag name", "class name", "css selector")，默认为None</td>
        <td rowspan="4">设置取element controls</td>
    </tr>
    <tr>
        <td>value: 与by配对使用，相应by的值</td>
    </tr>
    <tr>
        <td>index: 索引值，默认为0，即第一个， 如果by,value组合找到很多元素，通过索引index指定一个</td>
    </tr>
    <tr>
       <td>timeout: 超时时间，默认10，即10秒，如果by,value组合寻找元素超过10秒，超时报错</td>
   </tr>    
</table>
                                                   

### WebContext methods --> 用于上下文管理
```
DyAttrData(name,attr)                       # -> 属性-动态存储变量，适用于，保存UI元素属性值。name-变量名称，attr为UI元素的属性名称，**配合SetControl使用**
DyJsonData(name,sequence)                   # -> json-动态存储变量，适用于，保存页面返回json中的指定值。 name-变量名称，sequence是指访问json的序列串
                                                    示例,页面返回 {"a":1,
                                                            "b":[1,2,3,4],
                                                            "c":{"d":5,"e":6},
                                                            "f":{"g":[7,8,9]},
                                                            "h":[{"i":10,"j":11},{"k":12}]
                                                            }
                                                        DyJsonData("var1","a")      #var1值为 1
                                                        DyJsonData("var2","b.3")    #var2值为 4
                                                        DyJsonData("var3","f.g.2")  #var3值为 9
                                                        DyJsonData("var4","h.0.j")  #var4值为 11
DyStrData(name, regx, index)                # -> 字符串-动态存储变量，适用于，保存页面html中指定的值。 name-变量名称，regx已编译的正则表达式，index指定索引，默认0
GetAttribute(attr)                          # -> 获取元素指定属性的值， **配合SetControl使用**
GetText()                                   # -> 获取元素text值，**配合SetControl使用**
GetVar(name)                                # -> 获取指定变量的值
SetVar(name,value)                          # -> 设置指定变量的值
```

### WebWait methods --> 用于时间的控制
```
TimeSleep(seconds)                   # -> 指定等待时间(秒钟)
WaitForAppearing()                   # -> 等待元素出现(可能是隐藏，不可见的)，**配合SetControl使用**
WaitForDisappearing()                # -> 等待元素消失，**配合SetControl使用**
WaitForVisible()                     # -> 等待元素可见，**配合SetControl使用**
```

### WebVerify methods --> 用于验证
```
VerifyAlertText(text)                        # -> 验证alert弹窗，包含文本text
VerifyElemAttr(attr_name,expect_value)       # -> 验证元素属性attr_name的值，包含值expect_value,**配合SetControl使用**
VerifyElemCounts(num)                        # -> 验证元素数量为num,**配合SetControl使用**
VerifyElemEnabled()                          # -> 验证元素是enabled，**配合SetControl使用**
VerifyElemInnerHtml(expect_text)             # -> 验证元素innerHtml中，包含期望文本， **配合SetControl使用**
VerifyElemNotEnabled()                       # -> 验证元素是Not Enabled, **配合SetControl使用**
VerifyElemNotVisible()                       # -> 验证元素是不可见的，**配合SetControl使用**
VerifyElemVisible()                          # -> 验证元素是可见的， **配合SetControl使用**
VerifyTitle(title)                           # -> 验证浏览器标题为title
VerifyURL(url)                               # -> 验证浏览器当前url为期望值
```

### WebActions methods --> 用于浏览器操作
```
Alt(key)                     # -> 在指定元素上执行alt组合事件，**配合SetControl使用**
Backspace()                  # -> 在指定输入框发送回退键，**配合SetControl使用**
Click()                      # -> 在指定元素上，左键点击 1次，**配合SetControl使用**
ClickAndHold()               # -> 在指定元素上， 按压press住，**配合SetControl使用**
Ctrl(key)                    # ->  在指定元素上执行ctrl组合键事件，**配合SetControl使用**
DeSelectByIndex(index)       # -> 通过索引，取消选择下拉框选项，**配合SetControl使用**
DeSelectByText(text)         # -> 通过文本值，取消选择下拉框选项，**配合SetControl使用**
DeSelectByValue(value)       # -> 通过value值，取消选择下拉框选项，**配合SetControl使用**
DoubleClick()                # -> 鼠标左键点击2次，**配合SetControl使用**
Enter()                      # -> 在指定输入框发送回回车键,**配合SetControl使用**
Escape()                     # -> 在指定输入框发送回退出键,**配合SetControl使用**
Focus()                      # -> 在指定输入框发送 Null,用于设置焦点，**配合SetControl使用**
MouseOver()                  # -> 指定元素上，鼠标悬浮，**配合SetControl使用**
MoveAndDropTo()              # -> 暂不支持
ReleaseClick()               # -> 在指定元素上，释放按压操作，**配合SetControl使用**
RightClick()                 # -> 在指定元素上，鼠标右键点击1次，**配合SetControl使用**
SelectByIndex(index)         # -> 通过索引，选择下拉框选项，**配合SetControl使用**
SelectByText(text)           # -> 通过文本值，选择下拉框选项，**配合SetControl使用**
SelectByValue(value)         # -> 通过value值，选择下拉框选项，**配合SetControl使用**
SendKeys(value)              # -> 在指定元素上，输入文本，**配合SetControl使用**
Space()                      # -> 在指定元素上,发送空格，**配合SetControl使用**
Tab()                        # -> 在指定元素上,发送回制表键，**配合SetControl使用**
Upload(filename)             # -> 暂不支持。非原生，需要第三方工具
UploadType(file_path)        # -> 上传文件，仅原生file文件框, 如： <input type="file" ...>, **配合SetControl使用**
```


## 自定义，关键字(函数、变量)
> 在case同级目录中，创建  preference.py, 该文件所定义的 变量、函数，可以被动态加载和引用

执行用例的时候，可以使用 变量引用 或者关键字引用的方法，调用，自定义的函数和变量

```
# preference.py 示例

test_var = "hello rtsf."
def test_func():
    return "nihao rtsf."
 
```
