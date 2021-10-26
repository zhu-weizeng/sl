'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-05-20 17:42:47
LastEditors: Zhu Weizeng
LastEditTime: 2021-08-08 11:23:45
'''
import os
import requests
import datetime
from pyzwz.config import db_140
from pyzwz.zwz_db import db_engine
from pyzwz.zwz_gz import get_datelist, clear_floder, upload_data
from pyzwz.getcode import get_cookie


def get_first_last_day(date):
    month = date.month
    year = date.year
    first_day = datetime.date(year, month, 1)
    if month == 12:
        month = 0
        year = year + 1
    next_first_day = datetime.date(year, month+1, 1)
    last_day = next_first_day - datetime.timedelta(1)
    return first_day, last_day, next_first_day


def get_data(cookie, savepath, startdate, enddate):

    datelist = get_datelist(startdate, enddate)
    # for i in range(1000):
    #     first_day, last_day, next_first_day = get_first_last_day(startdate)
    #     datelist.append((first_day, last_day))
    #     startdate = next_first_day
    #     if next_first_day > enddate:
    #         break

    print(datelist)

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
    for i in range(len(datelist)//2):
        data = {
            'startDate': str(datelist[2*i]),
            'endDate': str(datelist[2*i+1]),
            'dateType': 2,
            'flowBusinessUnitId': '',
            'flowLegionId': '',
            'flowStudioId': '',
            'flowDepartId': '',
            'flowGroupId': '',
            'flowPm': '',
            'chargeMan': '',
            'siteId': '',
            'extendType': '',
            'adCode': '',
            'accountId': '',
            'promotionMethods': '',
            'vector': '',
            'callBusinessUnitId': '2010001,2100859,2110974',
            'legionCode': '',
            'quantumTransitionGroup': '',
            'promoteProject': '',
            'promoteProvince': '',
            'promoteCity': '',
            'site': '',
            'bizCardType': '',
            'quickView': 0,
            'specialClassFilterFlag': 'true',
            'isPrecludeBfData': 'false',
            'groupByColumn': 'siteId,chargeMan,flowPm,flowBusinessUnitCode,flowLegionCode,flowStudioCode,flowDepartCode,flowGroupCode,promotionTypeCode,advertisingAgencyCode,promotionMethodsCode,vectorCode,callBusinessUnitIdCode,callArmyCode,quantumTransitionGroupCode,promoteProjectCode,cardProvinceCode,cardCityCode,siteCode,bizCardTypeCode',
            'metricsColumn': 'cost,cash,roi,cpa,bizCardCost,visitCount,impression,click,cardNum,chance,signNum,nowWeekSignNum,flow,nowWeekFlow,onlineFlow,messageFlow,onlineCardNum,messageCardNum,onlineChance,messageChance,onlineSignNum,messageSignNum',
            'orderType': 'cash-desc',
            'sumType': 0
        }

        url_itemcode = ''

        respose = requests.post(url=url_itemcode, headers=headers, data=data)
        itemcode = eval(respose.text)['downloadItemCode']
        url = '{}'.format(
            itemcode)

        bdata = requests.get(url=url, headers=headers)

        path = savepath + '\\' + \
            str(datelist[2*i]) + '_' + \
            str(datelist[2*i+1]) + '_site_calling.csv'
        with open(path, 'wb') as fp:
            fp.write(bdata.content)
        print(path + ' 下载完成！')


def spider_site(day):
    columns = {
        '时间': 'everyday',
        '站点ID': 'site_id',
        '负责人': 'charge_man',
        '项目经理': 'project_mannager',
        '消费': 'spends',
        '现金': 'payments',
        '流水': 'transaction_amt_all',
        '当期流水': 'transaction_amt_this',
        '跨期流水': 'transaction_amt_pass',
        '在线流水': 'transaction_amt_online',
        '留言流水': 'transaction_amt_msg',
        '其他流水': 'transaction_amt_others',
        'ROI': 'roi_all',
        '展现量': 'ad_expose',
        '点击量': 'ad_click',
        'CPC': 'cpc_all',
        'CTR': 'ctr_all',
        '名片量': 'contacts_all',
        '在线名片量': 'contacts_online',
        '留言名片量': 'contacts_msg',
        '其他名片量': 'contacts_others',
        '名片成本': 'contact_cpa',
        '名片网销': 'contact_online_sales',
        '机会量': 'clues_all',
        '在线机会量': 'clues_online',
        '留言机会量': 'clues_msg',
        '其他机会量': 'clues_others',
        '录入率': 'entry_rate',
        'CPA': 'clue_cpa',
        '机会网销': 'clues_online_sales',
        '报名人数': 'enrollment_all',
        '当期报名人数': 'enrollment_this',
        '跨期报名人数': 'enrollment_pass',
        '报名单量': 'order_all',
        '当期报名单量': 'order_this',
        '跨期报名单量': 'order_pass',
        '在线报名单数': 'order_online',
        '留言报名单数': 'order_msg',
        '其他报名单数': 'order_others',
        '机会销转': 'clues_conversion_rate',
        '名片销转': 'contact_conversion_rate',
        '报名成本': 'enrollment_cost',
        '站点名称': 'site_nm',
        '流量事业部': 'traffic_business_unit',
        '流量军团': 'traffic_region',
        '工作室': 'traffic_studio',
        '项目部': 'traffic_depart',
        '项目组': 'traffic_group',
        '推广类型': 'promotion_cate',
        '广告商': 'advertiser',
        '账户': 'account',
        '推广方式': 'promotion_mode',
        '载体': 'ad_carrier',
        '事业部': 'traffic_center',
        '呼叫军团': 'calling_region',
        '量子跃迁团': 'quantum_region',
        '推广省份': 'province',
        '推广城市': 'city',
        '推广项目': 'product_sku',
        '网站': 'domain_name',
        '名片类型': 'contact_cate'
    }

    savepath = r'E:\zwz\zwz\python\spider_eagle\eagle_site_calling_data'
    savepath = savepath + '\\' + datetime.datetime.now().strftime('%y%m%d%H%M%S')
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    clear_floder(savepath)

    # 目前仍是手动更新cookie
    with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt', 'r') as f:
        dic_cookie = f.read()
    try:
        cookie = eval(dic_cookie)['eagle']
    except Exception as e:
        pass
    # startdate = datetime.date(2021, 1, 1)
    startdate = datetime.date.today() - datetime.timedelta(day)
    enddate = datetime.date.today()

    try:
        get_data(cookie, savepath, startdate, enddate)
    except Exception as e:
        print(e)
        print()
        cookies = get_cookie()
        with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt', 'w') as f:
            f.write(str(cookies))

        # cookie = input("Please input cookie:")
        # with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt', 'w') as f:
        #     f.write(cookie)
        cookie = cookies['eagle']
        get_data(cookie, savepath, startdate, enddate)

    engine = db_engine(db_140)
    conn = engine.connect()
    print("创建数据库连接，连接成功！")

    del_sql = "delete from sd_metis.log_eagle_site_calling_metis where everyday between '{}' and '{}';".format(
        startdate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d'))
    conn.execute(del_sql)
    print("删除成功：" + del_sql)

    delsql = "delete from sd_metis.log_eagle_site_calling_metis where site_id = '合计'"
    conn.execute(delsql)

    tablename = 'log_eagle_site_calling_metis'
    upload_data(savepath, conn, tablename, columns=columns)

    conn.close()
    engine.dispose()

    print(datetime.datetime.now())
    print()

# spider_site(5)
