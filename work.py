'''
Descripttion: 
version: 
Author: gujian
Date: 2021-05-26 11:52:29
LastEditors: Zhu Weizeng
LastEditTime: 2021-05-26 14:52:45
'''
import win32con
import win32api
import win32gui
import win32com
import pyperclip
from PIL import ImageGrab
from time import sleep
from win32com.client import Dispatch

# 调用win32api的模拟点击功能实现ctrl+v粘贴快捷键

def ctrlV():
    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(86, 0, 0, 0)  # v键位码是86
    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


# 调用win32api的模拟点击功能实现alt+s微信发送快捷键 （可以根据自己微信发送快捷键是什么来进行调整）
def altS():
    win32api.keybd_event(18, 0, 0, 0)  # Alt
    win32api.keybd_event(83, 0, 0, 0)  # s
    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)


# 调用win32gui调用桌面窗口，获取指定窗口句柄id,激活窗口  ，向函数传递窗口名称to_weixin
def wx_send(to_weixin):
    for i in range(0, len(to_weixin)):
        hw = win32gui.FindWindow(None, to_weixin[i])  # 获取窗口句柄
        win32gui.SetForegroundWindow(hw)  # 激活窗口
        sleep(1)
        ctrlV()
        sleep(2)
        altS()


def wkb_Operate(class_picture, wkb_path, sleep_time):  # 使win32调用excel,刷新数据并截图发送
    # os.system('taskkill /IM EXCEL.exe /F')
    xlapp = win32com.client.gencache.EnsureDispatch('Excel.Application')
    xlapp.Visible = 1
    xlapp.DisplayAlerts = False  # 关闭警告
    wkb = xlapp.Workbooks.Open(wkb_path)
    wkb.RefreshAll()
    sleep(sleep_time)
    print('文件【{}】已打开！'.format(wkb_path))
    try:
        for key, vlaue in class_picture.items():
            to_weixin = class_picture[key]['发送群']
            to_sontent = class_picture[key]['发送文本']
            sheet_name = class_picture[key]['sheetname']
            range_pic = class_picture[key]['图片区域']
            pyperclip.copy(to_sontent)
            wx_send(to_weixin)
            sheet_msg = wkb.Worksheets(sheet_name)
            sheet_msg.Range(range_pic).CopyPicture()
            wkb.Worksheets.Add().Name = 'picture'
            sheet_picture = wkb.Worksheets('picture')
            sleep(1)
            sheet_picture.Range('A1').Select()
            sheet_picture.Paste()
            sleep(1)
            xlapp.Selection.ShapeRange.Name = 'pic_name'
            sheet_picture.Shapes('pic_name').Copy()
            sleep(1)
            img = ImageGrab.grabclipboard()
            sleep(1)
            wx_send(to_weixin)
            wkb.Worksheets('picture').Delete()
            print('#粘贴 成功:%s', sheet_name)
    except BaseException as e:
        print(e)
        pass
    wkb.Save()
    wkb.Close(1)
    xlapp.Quit()
    print('#更新 成功:%s' % wkb_path)
    pass
