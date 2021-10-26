'''
Descripttion: 
version: 1.0
Author: Zhu Weizeng
Date: 2021-04-15 09:21:40
LastEditors: Zhu Weizeng
LastEditTime: 2021-07-18 11:09:56
'''
from pyzwz.zwz_spider import start_spider, upload_database
import datetime

dic_report = {
    '1': {'report_name': 'BF运营报表-多维度明细',
          'path': r'E:\zwz\zwz\python\spider_eagle\bf_operation_data',
          'conditions': {13: '墨提斯事业部,乌尔肯事业部,屋大维课堂'},
          'step': 30,
          'udb': [10, 140]},
    '2': {'report_name': '退费明细',
          'path': r'E:\zwz\zwz\python\spider_eagle\refund_data',
          'conditions': {4: '2100859,2010001,2110974'},
          'step': 30,
          'udb': [140]},
    '3': {'report_name': 'BF大课单-订单明细表',
          'path': r'E:\zwz\zwz\python\spider_eagle\bf_order_data',
          'conditions': {6: '墨提斯事业部,乌尔肯事业部,屋大维课堂'},
          'step': 30},
    '4': {'report_name': '订单明细表-有效订单',
          'path': r'E:\zwz\zwz\python\spider_eagle\order_data',
          'conditions': {},
          'step': 30,
          'udb': [140]},
    '5': {'report_name': '推广综合分析-站点明细-分日',
          'path': r'E:\zwz\zwz\python\spider_eagle\promote_site_data',
          'conditions': {},
          'step': 30,
          'udb': [140]},
    '6': {'report_name': '定金明细',
          'path': r'E:\zwz\zwz\python\spider_eagle\deposit_data',
                  'conditions': {},
                  'step':90,
          'udb': [10, 140]},
    '7': {'report_name': '',
          'path': r'',
                  'conditions': {},
                  'step': 10},
}


print(
    """
    1   BF运营报表-多维度明细
    2   退费明细
    3   BF大课单-订单明细表
    4   订单明细表-有效订单
    5   推广综合分析-站点明细-分日
    6   定金明细
    all 更新全部
    exit or 0
    """
)

# startdate = datetime.date(2019, 1, 1)
# enddate = datetime.date(2020, 1, 7)


def spider_upload(reportnum, startdate, enddate):
    report_name = dic_report[reportnum]['report_name']
    savepath = dic_report[reportnum]['path']
    conditions = dic_report[reportnum]['conditions']
    step = dic_report[reportnum]['step']
    if dic_report[reportnum].get('udb'):
        upload = dic_report[reportnum].get('udb')
    else:
        upload = [10]

    start_spider(savepath, report_name, startdate,
                 enddate, conditions, upload=upload, step=step)
    # upload_database(savepath, report_name, startdate, enddate, upload)
    print()


def main():
    startdate = datetime.date(2021, 1, 1)
    # startdate = datetime.date.today() - datetime.timedelta(20)
    enddate = datetime.date.today()

    while True:
        # reportnum = 'all'
        reportnum = input("Please input report id:")
        if reportnum == 'exit' or reportnum == '0':
            break
        elif reportnum == 'all':
            l_num = ['1', '2', '3', '4', '5','6']
            for i in l_num:
                spider_upload(i, startdate, enddate)
            break
        else:
            spider_upload(reportnum, startdate, enddate)
            pass


if __name__ == '__main__':
    main()
