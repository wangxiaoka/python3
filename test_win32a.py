# -*-encoding:utf-8 -*-
from time import sleep
import win32gui,win32con
import win32api
import win32com.client
import pymouse,pykeyboard

def _MyCallback(hwnd, extra):
    windows = extra
    temp = []
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        temp.append(hwnd)
        temp.append(win32gui.GetClassName(hwnd))
        temp.append(win32gui.GetWindowText(hwnd))
        windows[hwnd] = temp

def TestEnumWindows(title):
    windows = {}
    handle = 0
    win32gui.EnumWindows(_MyCallback, windows)
    print("Enumerated a total of  windows with %d classes", (len(windows)))
    print('------------------------------')
    # print classes
    for item in windows:
        print(windows[item])
        if title in windows[item][2]:
            handle = windows[item][0]
    print('-------------------------------')

    return handle

class cWindow:
    def __init__(self):
        self._hwnd = None
        self.shell = win32com.client.Dispatch("WScript.Shell")
    def BringToTop(self):
        win32gui.BringWindowToTop(self._hwnd)
    def SetAsForegroundWindow(self):
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(self._hwnd)
    def Maximize(self):
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)
    def setActWin(self):
        win32gui.SetActiveWindow(self._hwnd)
    def _window_enum_callback(self, hwnd, extra):
        '''Pass to win32gui.EnumWindows() to check all the opened windows'''
        # if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        #     self._hwnd = hwnd
        #     print(self._hwnd)
        windows = extra
        temp = []
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            temp.append(hwnd)
            temp.append(win32gui.GetClassName(hwnd))
            temp.append(win32gui.GetWindowText(hwnd))
            windows[hwnd] = temp
    def find_window_wildcard(self, wildcard):
        self._hwnd = None
        # win32gui.EnumWindows(self._window_enum_callback, wildcard)
        windows = {}
        win32gui.EnumWindows(_MyCallback, windows)
        print("Enumerated a total of  windows with %d classes", (len(windows)))
        print('------------------------------')
        # print classes
        for item in windows:
            # print(windows[item])
            if wildcard in windows[item][2]:
                print(windows[item])
                self._hwnd = windows[item][0]
        print('-------------------------------')

    def kill_task_manager(self):
        wildcard = 'Gestionnaire des t.+ches de Windows'
        self.find_window_wildcard(wildcard)
        if self._hwnd:
            win32gui.PostMessage(self._hwnd, win32con.WM_CLOSE, 0, 0)
            sleep(0.5)

class Mouse:
    def __init__(self):
        self.mouse = pymouse.PyMouse()
        self.x_dim, self.y_dim = self.mouse.position()



if __name__ == '__main__':
    title = 'FileZilla'
    # handle = TestEnumWindows(title)
    # print(handle)
    cW = cWindow()
    # cW.kill_task_manager()
    cW.find_window_wildcard(title)
    cW.SetAsForegroundWindow()
    cW.BringToTop()
    cW.Maximize()
    handle = cW._hwnd
    print(handle)
    # win32gui.MoveWindow(handle, 0, 0, 798, 537, False)
    edit = win32gui.WindowFromPoint((120, 80))
    print(edit)
    # win32api.SendMessage(edit, win32con.WM_SETTEXT, None, "abc")

    len = win32gui.SendMessage(edit, win32con.WM_GETTEXTLENGTH) + 1  # 获取edit控件文本长度
    buffer = win32gui.PyMakeBuffer(len)
    res = win32gui.SendMessage(edit, win32con.WM_GETTEXT, len, buffer)  # 读取文本
    print(res)
    print(buffer[:len - 1])
    address, length = win32gui.PyGetBufferAddressAndLen(buffer)
    text = win32gui.PyGetString(address, length)
    print(text)

    dlg = win32gui.FindWindowEx(handle, edit, "Edit", None)
    # dlg1 = win32gui.FindWindowEx(handle, dlg, "Edit", None)
    print(dlg)
    # print(dlg1)
    # buffer = '0' *50
    # len = win32gui.SendMessage(dlg, win32con.WM_GETTEXTLENGTH) + 1  # 获取edit控件文本长度
    # win32gui.SendMessage(dlg, win32con.WM_GETTEXT, len, buffer)  # 读取文本
    # print(buffer[:len - 1])
    # handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)

    mouse = pymouse.PyMouse()
    kb = pykeyboard.PyKeyboard()
    # print(mouse.position())
    host = [70, 81]
    user = [290, 86]
    pswd = [440, 87]
    hoststr = '192.168.0.108'
    userstr = 'kaka'
    pswdstr = '112358'
    for i in range(0):
        cW.SetAsForegroundWindow()
        cW.BringToTop()
        cW.Maximize()

        mouse.click(host[0],host[1],1,2)
        kb.type_string(hoststr)
        sleep(1)
        mouse.click(user[0],user[1],1,2)
        kb.type_string(userstr)
        sleep(1)
        mouse.click(pswd[0],pswd[1],1,2)
        kb.type_string(pswdstr)

        kb.tap_key(kb.enter_key)
        sleep(1.5)
        kb.tap_key(kb.enter_key)
    print('mark')