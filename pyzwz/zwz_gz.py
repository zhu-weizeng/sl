'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-03-25 10:49:45
LastEditors: Zhu Weizeng
LastEditTime: 2021-05-12 15:10:49
'''
import datetime
import os
from time import sleep
from win32com.client import Dispatch
import pandas as pd
from selenium.webdriver import Chrome


def get_datelist(startdate, enddate, step=6):
    datelist = [startdate.strftime('%Y-%m-%d')]
    for i in range(1, 1000):
        if i % 2 == 0:
            startdate += datetime.timedelta(1)
            datelist.append(startdate.strftime('%Y-%m-%d'))
        else:
            startdate += datetime.timedelta(step)
            datelist.append(startdate.strftime('%Y-%m-%d'))
        if startdate >= enddate and len(datelist) % 2 == 0:
            break

    # datelist = [datelist[2*i]+'-'+datelist[2*i+1]
    #             for i in range(len(datelist) // 2)]
    return datelist


def clear_floder(path):
    # 清空文件夹
    for root, dirs, files in os.walk(path, topdown=False):
        # print(root, dirs, files)
        for file in files:
            os.remove(root + '\\' + file)
        for dir in dirs:
            os.removedirs(root + '\\' + dir)
        print(path + ' 已清空')


def concat_data(path, addcol=None,drop=True):
    # 合并对应文件夹数据
    datalist = os.listdir(path)
    dflist = []

    for data in datalist:
        pdpath = path + '\\' + data
        if data.split('.')[-1] in ['xlsx', 'xls']:
            df = pd.read_excel(pdpath)
        elif data.split('.')[-1] == 'csv':
            df = pd.read_csv(pdpath, encoding='ansi')
        dflist.append(df)
    concatdata = pd.concat(dflist, join='outer', ignore_index=True)
    if drop:
        concatdata = concatdata.drop(concatdata.columns[[-1]], axis=1)

    if addcol:
        for k, v in addcol.item():
            concatdata[k] = v

    return concatdata


def upload_data(path, conn, tablename, col_flag=True, columns=None):
    # 获取文件名
    datalist = os.listdir(path)
    dflist = []

    for data in datalist:
        pdpath = path + '\\' + data
        if data.split('.')[-1] in ['xlsx', 'xls']:
            df = pd.read_excel(pdpath)
        elif data.split('.')[-1] == 'csv':
            df = pd.read_csv(pdpath, encoding='ansi', low_memory=False)
        dflist.append(df)
    concatdata = pd.concat(dflist, join='outer', ignore_index=True)
    if col_flag:
        concatdata = concatdata.drop(concatdata.columns[[-1]], axis=1)

    if columns:
        concatdata = concatdata[list(columns.keys())]
        concatdata = concatdata.rename(columns=columns)

    # 上传数据库
    concatdata.to_sql(name=tablename, con=conn,
                      if_exists='append', index=False)
    print(tablename + ' 上传成功')


def download_data(path, filename, conn, sql):
    df = pd.read_sql(sql=sql, con=conn)
    writer = pd.ExcelWriter(path + '\\' + filename)
    df.to_excel(writer, index=False)
    writer.save()
    print(filename + '下载完成！')


def create_table_by_excel(filepath, conn, table_name, drop_flag=False):
    # 自动建表
    if filepath.split('.')[-1] in ['xlsx', 'xls']:
        df = pd.read_excel(filepath)
    elif filepath.split('.')[-1] == 'csv':
        df = pd.read_csv(filepath, encoding='ansi')

    # 若drop_flag=True 则删表重建
    if drop_flag:
        drop_sql = "drop table if exists {};".format(table_name)
        conn.execute(drop_sql)

    sql = ''
    for col in df.columns:
        sql += col + " varcher(255) default null, "
    create_sql = "create table {} (".format(
        table_name) + sql[:-2] + ")engine=InnoDB DEFAULT CHARSET=utf8;"
    conn.execute(create_sql)


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
