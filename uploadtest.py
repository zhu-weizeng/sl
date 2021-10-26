'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-04-28 17:39:32
LastEditors: Zhu Weizeng
LastEditTime: 2021-07-02 18:23:52
'''
import pandas as pd
import os
from sqlalchemy import create_engine

# 修改改数据引擎
engine = create_engine(
    "mysql+pymysql://{username}:{password}@{host}/{database}".format(
        username='', password='', host='', database='')
)
conn = engine.connect()

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

def upload_data(path, conn, tablename,columns=None):
    # 获取文件名
    datalist = os.listdir(path)
    print(datalist)
    
    for data in datalist:
        pdpath = path + '\\' + data
        if data.split('.')[-1] in ['xlsx', 'xls']:
            df = pd.read_excel(pdpath)
        elif data.split('.')[-1] == 'csv':
            df = pd.read_csv(pdpath, encoding='ansi')
        df = df.iloc[:,:]
        if columns:
            df = df[columns.keys()]
            df = df.rename(columns=columns)
        df.to_sql(name=tablename, con=conn,
                    if_exists='append', index=False)
        print(pdpath + ' 上传成功！')

    # 上传数据库
    print(tablename + '上传成功')


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

    # 创建表
    sql = ''
    for col in df.columns:
        sql += "`" + col + "` varcher(255) default null, "
    create_sql = "create table {} (".format(
        table_name) + sql[:-2] + ")engine=ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    conn.execute(create_sql)


# 上传excel范例

# 数据所在的文件夹（相同类型的数据文件可以自动合并）
# path = r'E:\zwz\zwz\python\spider_eagle\eagle_site_calling_data'
# tablename = "log_eagle_site_calling_metis"
# upload_data(path, conn, tablename,columns)

# path = r'C:\Users\1\Desktop\eagle_site_calling'
# tablename = "log_eagle_site_calling_metis"
# upload_data(path, conn, tablename)

# 插入t_od_br
path = r'C:\Users\1\Desktop\2107 换签后军团映射\a'
tablename = 't_od_br'
upload_data(path, conn, tablename,columns=None)

conn.close()
engine.dispose()
