'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-08-16 17:15:20
LastEditors: Zhu Weizeng
LastEditTime: 2021-08-18 15:57:29
'''
# font_sizes.py
import openpyxl
from openpyxl.styles import Font
import asyncio


def font_demo(path):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    cell = sheet["A1"]
    cell.font = Font(size=12)
    cell.value = "Hello"
    cell2 = sheet["A2"]
    cell2.font = Font(name="Arial", size=14, color="00FF0000")
    sheet["A2"] = "from"
    cell2 = sheet["A3"]
    cell2.font = Font(name="Tahoma", size=16, color="00339966")
    sheet["A3"] = "OpenPyXL"
    workbook.save(path)


if __name__ == "__main__":
    font_demo("font_demo.xlsx")

{

}
