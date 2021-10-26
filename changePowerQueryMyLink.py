'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-07-07 10:10:42
LastEditors: Zhu Weizeng
LastEditTime: 2021-07-07 11:17:13
'''
import os
from win32com.client import Dispatch
from time import sleep

filepath = r'E:\zwz\weekly_copy'
dirs = os.listdir(filepath)
print(dirs)
app = Dispatch('Excel.Application')
for path in dirs:
    print(path)
    if path.split(".")[-1] in ['xls','xlsx']:
        workbook = app.Workbooks.Open(filepath + '\\' + path)
        for pq in workbook.Queries:
            # pq.Formula = pq.Formula.replace("10.248.62.72:63306", "10.247.63.82:63306")
            # "ReturnSingleDatabase=true, "
            pq.Formula = pq.Formula.replace("ReturnSingleDatabase=true, ", "")
            pq.Formula = pq.Formula.replace(", ReturnSingleDatabase=true", "")
            # print(pq.Formula)
        workbook.Save()
        sleep(1)
        workbook.Close()
        sleep(1)
        print("更改完成{}".format(path))
app.Quit()
