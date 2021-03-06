from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import json
import requests
import datetime
import os
from time import sleep
from random import randint
from pyzwz.config import db_10, db_140, report, headers
from pyzwz.zwz_db import db_engine
from pyzwz.zwz_gz import clear_floder, upload_data, get_datelist
from pyzwz.getcode import get_cookie


def get_downloadInfo(report_name, conditions):
    dic_payload = report[report_name]['payloaddata']
    for k, v in conditions.items():
        dic_payload['conditions'][k]['condition_value'] = v
    jpayload = json.dumps(dic_payload)

    url = 'http://**/eagle-metabase/api/metabase/putDownloadParams'
    response = requests.post(url=url, headers=headers, data=jpayload)
    downloadItemCode = json.loads(response.text)["data"]
    reportid = report[report_name]['reportid']
    return reportid, downloadItemCode


def get_eagle_data(reportid, downloadItemCode):
    download_url = 'http://**/eagle-metabase/api/metabase/queryReportXYDownload?id=' + \
        reportid + '&conditions=' + downloadItemCode
    data = requests.get(url=download_url, headers=headers).content
    return data


def save_eagle_data(data, path, filename):
    filepath = path + '\\' + filename
    with open(filepath, 'wb') as fp:
        fp.write(data)


def upload_database(path, report_name, startdate, enddate, upload):
    # if upload == 10:
    #     engine = db_engine(db_10)
    # else:
    #     engine = db_engine(db_140)

    for num in upload:
        if num == 10:
            engine = db_engine(db_10)
        elif num == 140:
            engine = db_engine(db_140)
        else:
            break
        print('----------开始导入' + str(num) + '库----------')
        conn = engine.connect()
        tablename = report[report_name]['dbtable']
        datename = report[report_name]['datename']
        del_sql = "delete from sd_metis.{} where date({}) between '{}' and '{}'".format(tablename, datename,
                                                                                        str(startdate), str(enddate))
        conn.execute(del_sql)
        print(del_sql)
        dic_rename = report[report_name]['transcolumns']
        upload_data(path, conn, tablename, columns=dic_rename)
        del_sql = "delete from sd_metis.{} where {} = '合计'".format(
            tablename, datename)
        conn.execute(del_sql)
        conn.close()
        engine.dispose()
        print(datetime.datetime.now())


def start_spider(path, report_name, startdate, enddate, conditions, upload=None, step=6):
    datelist = get_datelist(startdate, enddate, step)
    path = path + '\\' + datetime.datetime.now().strftime('%y%m%d%H%M%S')
    if not os.path.exists(path):
        os.mkdir(path)
    clear_floder(path)
    with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt', 'r') as f:
        dic_cookie = f.read()
    try:
        headers['Cookie'] = eval(dic_cookie)['bi']
    except Exception as e:
        print(e)
    for i in range(len(datelist) // 2):
        conditions[0] = datelist[2*i] + ',' + datelist[2*i+1]

        try:
            reportid, downloadItemCode = get_downloadInfo(
                report_name, conditions)
        except Exception as e:
            print(e)
            try:
                cookies = get_cookie()
            except Exception as e:
                cookies = get_cookie()
            with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt', 'w') as f:
                f.write(str(cookies))

            headers['Cookie'] = cookies['bi']
            # headers['Cookie'] = input("Please input cookie: ")
            reportid, downloadItemCode = get_downloadInfo(
                report_name, conditions)
            # with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt', 'w') as f:
            #     f.write(headers['Cookie'])

        data = get_eagle_data(reportid, downloadItemCode)
        sleep(randint(1, 5))
        filename = report_name + '_' + \
            datelist[2*i] + '_' + datelist[2*i+1] + '.csv'
        save_eagle_data(data, path, filename)
        print(filename + '保存成功')

    if upload:
        upload_database(path, report_name, datelist[0], datelist[-1], upload)
