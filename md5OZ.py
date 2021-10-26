'''
Descripttion: 
version: 
Author: Zhu Weizeng
Date: 2021-06-28 10:29:27
LastEditors: Zhu Weizeng
LastEditTime: 2021-06-29 10:20:12
'''
import hashlib
string1 = 'wechat'
md = hashlib.md5()
md.update(string1.encode('utf-8'))
print(md.hexdigest())