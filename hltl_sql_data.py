'''
Descripttion: 1.1
version: 1.1
Author: Zhu Weizeng
Date: 2021-07-13 16:55:50
LastEditors: Zhu Weizeng
LastEditTime: 2021-08-19 16:58:57
'''
from sqlalchemy import engine
from pyzwz.config import db_172
from pyzwz.zwz_db import db_engine
import pandas as pd
import datetime
import os

engine = db_engine(db_172)
conn = engine.connect()

path = r'E:\zwz\work\狐逻&泰罗\data' + '\\' + '狐逻&泰罗 ' + \
    datetime.date.today().strftime('%y%m%d')
if not os.path.exists(path):
    os.mkdir(path)

sql_path = r'E:\zwz\work\狐逻&泰罗\sql'
sql_dir = os.listdir(sql_path)
print(sql_dir)
for sql_name in sql_dir:
    sql_filename = sql_path + '\\' + sql_name
    with open(sql_filename, 'r', encoding='utf-8') as fp:
        sql_text = fp.read()
    sql_text = sql_text.replace('2021-07-01 00:00:00', '2021-08-01 00:00:00')
    df = pd.read_sql(sql_text, con=conn)
    pathfile = path + '\\' + '狐逻&泰罗 ' + sql_name.split('.')[0] + ' ' + \
        datetime.date.today().strftime('%y%m%d') + '.xls'
    print(pathfile)
    writer = pd.ExcelWriter(pathfile)
    df.to_excel(writer, index=False, engine='xlwt')
    writer.save()

conn.close()
engine.dispose()
print(datetime.datetime.now())
