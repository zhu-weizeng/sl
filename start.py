'''
Descripttion: 
version: 
Author: gujian
Date: 2021-05-26 14:41:40
LastEditors: Zhu Weizeng
LastEditTime: 2021-05-26 14:54:11
'''
import work

def file_metisjiankong():
    path_process = r"E:\zwz\auto_work\od_pk_211_king.xlsx"  # 文件夹路径
    class_picture1 = {'pic1':{'发送群':['朱伟增 - 工作号'],'sheetname':'展示','图片区域':'A1:G44','发送文本':'截止到目前的流水和PK情况'}}
    work.wkb_Operate(class_picture1,path_process,8)

# file_metisjiankong()