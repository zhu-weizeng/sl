import requests
from selenium.webdriver import Chrome
from random import randint
from time import sleep
from selenium.webdriver.chrome.options import Options
import datetime

def get_cookie(bro):
    bro.get("")

    sleep(10)

    if '统一登录中心' in bro.page_source:
        bro.find_element_by_xpath('//*[@id="password"]').send_keys('134025')
        sleep(1)
        bro.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[2]/input[7]').click()
    
    sleep(10)
    
    bro.get("")

    cookies = {}
    bro.get("")
    cookie = bro.get_cookies()
    cookies['eagle'] = cookie[0]['name']+'='+cookie[0]['value']
    sleep(3)

    bro.get("")
    sleep(5)
    bro.get("")
    cookie = bro.get_cookies()
    cookies['bi'] = cookie[0]['name']+'='+cookie[0]['value']
    sleep(3)

    bro.get("")
    # bro.quit()
    with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\cookies.txt','w') as fp:
        fp.write(str(cookies))
    with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\eaglecookie.txt','w') as fp1:
        fp1.write(str(cookies['eagle']))
    with open(r'E:\zwz\zwz\python\spider_eagle\cookietxt\twicecookie.txt','w') as fp2:
        fp2.write(str(cookies['bi']))
    return cookies

if __name__ == '__main__':
    chrome_options = Options()
    bro = Chrome(executable_path=r"E:\zwz\zwz\python\chromedriver.exe",chrome_options=chrome_options)

    while True:
        try:
            get_cookie(bro)
        except Exception as e:
            get_cookie(bro)
        if datetime.datetime.now().strftime('%H') == '00':
            bro.quit()
        print(datetime.datetime.now())
        sleep(randint(1740,1800))
