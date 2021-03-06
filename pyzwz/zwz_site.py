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
        print(path + ' ???????????????')


def spider_site(day):
    columns = {
        '??????': 'everyday',
        '??????ID': 'site_id',
        '?????????': 'charge_man',
        '????????????': 'project_mannager',
        '??????': 'spends',
        '??????': 'payments',
        '??????': 'transaction_amt_all',
        '????????????': 'transaction_amt_this',
        '????????????': 'transaction_amt_pass',
        '????????????': 'transaction_amt_online',
        '????????????': 'transaction_amt_msg',
        '????????????': 'transaction_amt_others',
        'ROI': 'roi_all',
        '?????????': 'ad_expose',
        '?????????': 'ad_click',
        'CPC': 'cpc_all',
        'CTR': 'ctr_all',
        '?????????': 'contacts_all',
        '???????????????': 'contacts_online',
        '???????????????': 'contacts_msg',
        '???????????????': 'contacts_others',
        '????????????': 'contact_cpa',
        '????????????': 'contact_online_sales',
        '?????????': 'clues_all',
        '???????????????': 'clues_online',
        '???????????????': 'clues_msg',
        '???????????????': 'clues_others',
        '?????????': 'entry_rate',
        'CPA': 'clue_cpa',
        '????????????': 'clues_online_sales',
        '????????????': 'enrollment_all',
        '??????????????????': 'enrollment_this',
        '??????????????????': 'enrollment_pass',
        '????????????': 'order_all',
        '??????????????????': 'order_this',
        '??????????????????': 'order_pass',
        '??????????????????': 'order_online',
        '??????????????????': 'order_msg',
        '??????????????????': 'order_others',
        '????????????': 'clues_conversion_rate',
        '????????????': 'contact_conversion_rate',
        '????????????': 'enrollment_cost',
        '????????????': 'site_nm',
        '???????????????': 'traffic_business_unit',
        '????????????': 'traffic_region',
        '?????????': 'traffic_studio',
        '?????????': 'traffic_depart',
        '?????????': 'traffic_group',
        '????????????': 'promotion_cate',
        '?????????': 'advertiser',
        '??????': 'account',
        '????????????': 'promotion_mode',
        '??????': 'ad_carrier',
        '?????????': 'traffic_center',
        '????????????': 'calling_region',
        '???????????????': 'quantum_region',
        '????????????': 'province',
        '????????????': 'city',
        '????????????': 'product_sku',
        '??????': 'domain_name',
        '????????????': 'contact_cate'
    }

    savepath = r'E:\zwz\zwz\python\spider_eagle\eagle_site_calling_data'
    savepath = savepath + '\\' + datetime.datetime.now().strftime('%y%m%d%H%M%S')
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    clear_floder(savepath)

    # ????????????????????????cookie
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
    print("???????????????????????????????????????")

    del_sql = "delete from sd_metis.log_eagle_site_calling_metis where everyday between '{}' and '{}';".format(
        startdate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d'))
    conn.execute(del_sql)
    print("???????????????" + del_sql)

    delsql = "delete from sd_metis.log_eagle_site_calling_metis where site_id = '??????'"
    conn.execute(delsql)

    tablename = 'log_eagle_site_calling_metis'
    upload_data(savepath, conn, tablename, columns=columns)

    conn.close()
    engine.dispose()

    print(datetime.datetime.now())
    print()

# spider_site(5)
