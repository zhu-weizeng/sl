'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-05-20 17:29:47
LastEditors: Zhu Weizeng
LastEditTime: 2021-07-15 09:40:01
'''
import requests
from selenium.webdriver import Chrome
import pandas as pd
from time import sleep
from random import randint
import datetime
import os
from pyzwz.config import db_140
from pyzwz.zwz_db import db_engine
from pyzwz.zwz_gz import get_datelist, upload_data
from pyzwz.getcode import get_cookie


# bro = Chrome()
# bro.get()


def get_yysdata(cookie, savepath, startdate, enddate):
    # UA伪装，请求headers
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 更新筛选项
    url_sc = ''

    # post form_data
    form_data = {
        'businessType': 'salesreport',
        'selectedKeys': 'cost,cash,cjPhoneNumDay,fpPhoneNumDay,chance,chanceValidRate,visitNum,nowWeekVisit,lastWeekVisit,interTimeVisit,returnVisitRate,nowWeekReturnVisitRate,interTimeReturnVisitRate,visitPersonNum,nowWeekVisitPerson,lastWeekVisitPerson,interTimeVisitPerson,reservationNum,nowWeekReservationNum,interTimeReservationNum,reservationToCurrent,signPersonNum,nowWeekSign,interTimeSign,signNum,nowWeekSignNum,interTimeSignNum,flow,nowWeekFlow,lastWeekFlow,interTimeFlow,cardTransfer,transfer,thisWeekTransfer,interTimeTransfer,arpu,nowWeekARPU,interTimeARPU,rpa,refundFlow,callNum,talkTime,avgTalkTime,incomingCallNum,incomingTalkTime,exhaleCallNum,exhaleTalkTime,incomingEffCallNum,exhaleEffCallNum,exhaleSuccessRate,firstcallValidTime,weekcallValidTime,intertimecallValidTime'
    }

    # 发送更新请求
    requests.post(url=url_sc, headers=headers, data=form_data)

    # 分日期下载
    datelist = get_datelist(startdate, enddate)
    print('日期时间段为：', datelist)
    datelist = [datelist[2*i]+'-'+datelist[2*i+1]
                for i in range(len(datelist) // 2)]

    for d in datelist:
        data = {
            'businessCode': '2010001,2100859,2110974',
            'legionCode': '',
            'callMatrixCode': '',
            'departCode': '',
            'groupCode': '',
            'consultantCode': '',
            'extendType': '',
            'advertiseCode': '',
            'registProvince': '',
            'registSKU': '',
            'promoteProvince': '',
            'promoteCity': '',
            'promoteType': '',
            'organType': '6',
            'dateType': '1',
            'date': d,
            'orderType': 'flow-desc',
            'sumType': '0',
            'specialClassFilterFlag': 'true',
            'isPrecludeBfData': 'false'
        }

        # 获取downloadItemCode，进一步进行下载数据
        url_getdic = ''
        response = requests.post(url=url_getdic, headers=headers, data=data)
        # print(response.text)
        download_item_code = eval(response.text)['downloadItemCode']
        # print(download_item_code)
        # sleep(randint(1, 5))

        # 获取下载结果
        url = '{}'.format(
            download_item_code)
        rpdata = requests.get(url=url, headers=headers).content

        # 持久化存储
        filepath = savepath + '\\' + d + '.csv'
        with open(filepath, 'wb') as fp:
            fp.write(rpdata)
        print(d + '.csv下载成功')
        sleep(randint(1, 5))


def clear_floder(path):
    # 清空历史数据文件夹
    for root, dirs, files in os.walk(path, topdown=False):
        # print(root, dirs, files)
        for file in files:
            os.remove(root + '\\' + file)
        for dir in dirs:
            os.removedirs(root + '\\' + dir)
        print(path + ' 已清空')


# def upload_data(path, conn, tablename):
#     datalist = os.listdir(path)
#     dflist = []
#     for data in datalist:
#         pdpath = path + '\\' + data
#         df = pd.read_csv(pdpath, encoding='ansi')
#         dflist.append(df)
#     concatdata = pd.concat(dflist, join='outer', ignore_index=True)
#     concatdata = concatdata.drop(concatdata.columns[[-1]], axis=1)

#     concatdata.to_sql(name=tablename, con=conn,
#                       if_exists='append', index=False)
#     print("上传完成！")


def spider_pk(day):
    savepath = r'E:\zwz\zwz\python\spider_eagle\eagle_pk_data'
    savepath = savepath + '\\' + datetime.datetime.now().strftime('%y%m%d%H%M%S')
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    clear_floder(savepath)

    columns = {
        '日期': 'everyday',
        '事业部名称': 'department',
        '呼叫军团名称': 'corpus',
        '量子跃迁团': 'corpus_team',
        '销售部': 'sales_corpus',
        '销售组': 'sales_team',
        '咨询师EM': 'consultant_EM',
        '咨询师': 'consultant',
        '推广费': 'spends',
        '现金': 'payments',
        '创建名片数': 'card_create',
        '分配总名片数': 'card_total',
        '销售机会数': 'sale_change_num',
        '机会有效率': 'chance_effect',
        '回访数': 'back_num',
        '当周回访数': 'back_num_week',
        '上周回访数': 'back_num_last_week',
        '跨期回访数': 'back_inter',
        '回访比': 'back_pro',
        '当周回访比': 'back_week_pro',
        '跨期回访比': 'back_inter_pro',
        '总回访人数': 'back_total_num',
        '当周回访人数': 'back_week_num',
        '上周回访人数': 'back_last_week_num',
        '跨期回访人数': 'back_inter_num',
        '预约单数': 'order_num_pre',
        '当周预约单数': 'order_num_pre_week',
        '跨期预约单数': 'order_num_pre_inter',
        '预约至当前单数': 'order_num_today',
        '报名人数': 'sign_up_num',
        '当周报名人数': 'sign_up_week',
        '跨期报名人数': 'sign_up_inter',
        '报名单数': 'sign_num',
        '当周报名单数': 'sign_num_week',
        '跨期报名单数': 'sign_num_inter',
        '流水': 'cash',
        '当周流水': 'cash_week',
        '上周流水': 'cash_last_week',
        '跨期（减上周）流水': 'cash_inter',
        '名片销转': 'sale_card',
        '机会销转': 'sale_chance',
        '当周机会销转': 'sale_change_week',
        '跨期机会销转': 'sale_change_week_inter',
        'ARPU': 'arpu',
        '当周ARPU': 'arpu_week',
        '跨期ARPU': 'arpu_week_inter',
        '效率值': 'effect_num',
        '退费': 'refund',
        '通话个数': 'call_num',
        '通话时长': 'call_time',
        '平均通话时长': 'call_time_avg',
        '呼入通话个数': 'call_in_num',
        '呼入通话时长': 'call_in_time',
        '呼出通话个数': 'call_out_num',
        '呼出通话时长': 'call_out_time',
        '呼入有效通话个数': 'call_in_effect',
        '呼出有效通话个数': 'call_out_effect_num',
        '呼出成功率': 'call_out_success',
        '首咨有效时长': 'sz_call_time',
        '当周有效时长': 'week_call_time',
        '跨期有效时长': 'week_inter_call_time'
    }

    # 目前仍是手动更新cookie
    with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt', 'r') as f:
        dic_cookie = f.read()
    # startdate = datetime.date(2021, 1, 1)
    startdate = datetime.date.today() - datetime.timedelta(day)
    enddate = datetime.date.today()
    try:
        cookie = eval(dic_cookie)['eagle']
    except Exception as e:
        pass

    try:
        get_yysdata(cookie, savepath, startdate, enddate)
    except Exception as e:
        print(e)
        print()

        cookies = get_cookie()
        with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt', 'w') as f:
            f.write(str(cookies))

        cookie = cookies['eagle']
        # cookie = input("Please input cookie:")
        # with open('./spider_eagle/cookietxt/eaglecookie.txt', 'w') as f:
        #     f.write(cookie)
        get_yysdata(cookie, savepath, startdate, enddate)

    engine = db_engine(db_140)
    conn = engine.connect()
    print("创建数据库连接，连接成功！")

    del_sql = "delete from sd_metis.log_eagle_pk_metis where everyday between '{}' and '{}';".format(
        startdate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d'))
    conn.execute(del_sql)
    print("删除成功：" + del_sql)

    delsql = "delete from sd_metis.log_eagle_pk_metis where department = '合计'"
    conn.execute(delsql)

    tablename = 'log_eagle_pk_metis'
    upload_data(savepath, conn, tablename, columns=columns)

    conn.close()
    engine.dispose()

    print(datetime.datetime.now())
    print()


# spider_pk(5)
