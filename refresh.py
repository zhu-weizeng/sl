'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-07-07 18:46:11
LastEditors: Zhu Weizeng
LastEditTime: 2021-07-07 19:04:30
'''
from PIL import ImageGrab
import xlwings as xw
import datetime


def excel_refresh(shot_excel):
    app = xw.App(visible=True, add_book=False)
    wb = app.books.open(shot_excel)
    wb.api.RefreshAll()
    wb.save()
    # app.quit()

# excel = r'E:\zwz\weekly_copy\Amoeba.xlsx'
# excel_refresh(excel)

