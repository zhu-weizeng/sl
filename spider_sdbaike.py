'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-07-30 18:07:16
LastEditors: Zhu Weizeng
LastEditTime: 2021-07-30 18:07:17
'''
'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-07-30 18:07:16
LastEditors: Zhu Weizeng
LastEditTime: 2021-07-30 18:07:16
'''
import requests
import pandas as pd
url = 'https://klib.ministudy.com/k-lib/c/kt/selfExam/list'
data = {
    'provinceCode': 1,
    'pageNo': 1,
    'pageSize': 10,
}
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://klib.ministudy.com/k-lib/',
    'Cookie': ''
}

df_major = []
df_sublist = []
count = 0
for i in range(1,33):
    data['provinceCode'] = i
    resp = requests.post(url=url,data=data,headers=headers)
    df_dict = eval(resp.text)['data']['resultList']
    df = pd.DataFrame(df_dict)
    df_major.append(df)

    for index,sublist in enumerate(df_dict):
        df_sub_dict = df_dict[index]['subList']
        df_sub = pd.DataFrame(df_sub_dict)
        df_sublist.append(df_sub)
    
    count += 1
    print(count)

df_major_concat = pd.concat(df_major,join='outer',ignore_index=True)
df_sublist_concat = pd.concat(df_sublist,join='outer',ignore_index=True)
df_major_concat.to_csv(r'C:\Users\1\Downloads' + '\\' + 'major.csv', encoding='ansi', index=False)
df_sublist_concat.to_csv(r'C:\Users\1\Downloads' + '\\' + 'sunlist.csv', encoding='ansi', index=False)