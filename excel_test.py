'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-06-03 11:31:39
LastEditors: Zhu Weizeng
LastEditTime: 2021-06-03 14:37:28
'''
from PIL import ImageGrab
import xlwings as xw
import datetime


def excel_catch_screen(shot_excel, shot_sheetname):
    app = xw.App(visible=True,  add_book=False)
    wb = app.books.open(shot_excel)
    wb.api.RefreshAll()
    sheet = wb.sheets(shot_sheetname)
    all = sheet.used_range
    # print(all.value)
    all.api.CopyPicture()
    sheet.api.Paste()
    img_name = (shot_excel.split('.')[0]).split(
        '\\')[-1] + str(datetime.datetime.today().strftime(' %Y_%m_%d_%H_%M_%S'))
    pic = sheet.pictures[0]
    pic.api.Copy()
    img = ImageGrab.grabclipboard()
    img.save(r"C:\Users\1\Desktop\新建文件夹" + '\\' + img_name + ".png")
    pic.delete()
    wb.save()
    wb.close()
    app.quit()


shot_excel = r'C:\Users\1\Desktop\新建文件夹\公众号增粉.xlsx'
shot_sheetname = '展示'
excel_catch_screen(shot_excel, shot_sheetname)
