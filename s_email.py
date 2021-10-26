'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-07-20 18:19:40
LastEditors: Zhu Weizeng
LastEditTime: 2021-07-21 10:13:25
'''
import zmail
from win32com.client import Dispatch
from time import sleep
import os
import datetime


def refresh_excel(path):
    def refresh_path(pathfile):
        xlapp = Dispatch('Excel.Application')
        xlapp.Visible = 1
        wkb = xlapp.Workbooks.Open(pathfile, False, False, None, 'site2019')
        sleep(5)
        wkb.RefreshAll()
        sleep(5)
        wkb.Save()
        sleep(3)
        wkb.Close(1)
        sleep(3)
        xlapp.Quit()

    if path.split('.')[-1] == 'xlsx':
        refresh_path(path)
    else:
        for file in os.listdir(path):
            if file.split('.')[-1] == 'xlsx' and '~' not in file:
                pathfile = path + '\\' + file
                refresh_path(pathfile)
    print('自动更新结束')


# 需要刷新并发送的文件目录
path = r'E:\zwz\email\学历班型监控-W30.xlsx'
refresh_excel(path)

server = zmail.server('zhuweizeng@wdwedu.cn', email_up())

mail = {
    'from': 'zhuweizeng@wdwedu.cn',
    'subject': '学历班型情况_刷新日期为' + str(datetime.date.today()),
    'content_text': '附件为学历班型报表',
    # 'attachments': [path + '\\' + file for file in os.listdir(path) if file.split('.')[-1] == 'xlsx' and '~' not in file],
    'attachments': [path],
}

to_add = []
# to_add = ['zhuweizeng@wdwedu.cn']

# 抄送人
cc_add = ['zhuweizeng@wdwedu.cn']

server.send_mail(recipients=to_add, mail=mail, cc=cc_add)
print(path + "发送成功！！")
sleep(5)
