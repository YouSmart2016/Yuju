import requests
from bs4 import BeautifulSoup
import time
import random
from fake_useragent import UserAgent
import json
import re
import urllib



#    {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Cookie': 'yunsuo_session_verify=298113650b741ded365074658802d145; __gads=ID=193c2701cb325c0f:T=1579862271:S=ALNI_MYZHoq_-2vRjkyEYSU2LQhKR4h3Xw; UM_distinctid=16fd7211d8e8af-0eb4c47cff4775-b383f66-144000-16fd7211d8f7d7; Hm_lvt_d3c4d55d22641d9ba073fe8bfa9afdf7=1579862269,1579930282; CNZZDATA1132471=cnzz_eid%3D1427959062-1579858793-null%26ntime%3D1579928673; Hm_lpvt_d3c4d55d22641d9ba073fe8bfa9afdf7=1579932347',
    'Host': 'www.00394.net'
    }

def analyseList(url):
    local_path='H:/BaiduNetdiskDownload/zhuizi/'
    print('正在爬取豫剧列表：',url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.content
        try:
            html = html.decode(encoding='gb2312')
        except Exception as ex:
            html=html.decode(encoding='gbk')
        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.find(class_="e2").children
        _time=time.time()
        x=0
        for item in lis:
            downUrl=''
            try:
                if(item):
                    href= item.select('.title')[0].attrs['href']
                    songName= item.select('.title')[0].get_text()
                    #lastIndex=href.rfind('/')+1
                    #id= href[lastIndex:lastIndex+5]
                    id=re.search(r'[\d]+.html',href)[0].split('.')[0]
                    downUrl='http://www.00394.net/plus/download.php?open=0&aid={}&cid=3'
                    downUrl=downUrl.format(str(id))
                    print('正在下载：',downUrl)
                    res=requests.get(downUrl, headers=headers)
                    if(res.status_code==200):
                        html = res.content
                        html = html.decode(encoding='gb2312')
                        soup = BeautifulSoup(html, 'html.parser')
                        downurl=soup.find(class_="xq_down_co").select('a')[0].attrs['href']
                        headersDown={
                        'Host':'00394-10012740.file.myqcloud.com',
                        'Connection':'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Referer':'http://www.00394.net/plus/download.php?open=0&aid={}&cid=3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9'
                               }
                        chinaURl=urllib.request.quote(downurl, safe=";/?:@&=+$,()", encoding="utf-8")
                        resDown=requests.get(chinaURl, headers=headersDown)
                        if(resDown.status_code==200):
                            cont = resDown.content
                            open(local_path + '%s.mp3' % songName, 'wb').write(cont)
                        x+=1
            except Exception as ex:
                print('报错下载页面：',downUrl,ex)

def createUrl(pageIndex):
    url='http://www.00394.net/xiqump3/zhuizi/list_89_{}.html'
    #url = 'http://www.00394.net/xiqump3/yuju/list_87_{}.html'
    return url.format(str(pageIndex))


def startScrapy(start=1,end=23):
    for n in range(start,end):
        try:
            analyseList(createUrl(n))
        except Exception as ex:
                print('发生异常：',ex)
startScrapy(1,11)  