#-*- coding:utf-8 -*-
#CREATER: NTGtech-ShenAo
import NTG_base

from lxml import etree
import json
import subprocess
import requests
def GetVidInf(VidID, proxy):
    Url = 'https://www.youtube.com/watch?v=' + VidID
    header = {
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'service-worker-navigation-preload': 'true',
        'upgrade-insecure-requests': '1',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': '',#Your cookie here
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52',
    }
    
    result = NTG_base.get(Url, header, '', proxy)[0]
    tree = etree.HTML(result)
    #视频名称
    VidName = tree.xpath('/html/head/title/text()')[0].replace(' - YouTube', '')
    VidName = NTG_base.process_file_name(VidName)
    VidInf = tree.xpath('/html/body/script[1]/text()')[0]
    #格式化为json可以看懂的
    VidInf = VidInf.replace('var ytInitialPlayerResponse = ', '').replace(';var meta = document.createElement(\'meta\'); meta.name = \'referrer\'; meta.content = \'origin-when-cross-origin\'; document.getElementsByTagName(\'head\')[0].appendChild(meta);', '')
    #能拿到的最高清画质
    VidLink = json.loads(VidInf)['streamingData']['formats'][-1]['url']     
    return VidLink, VidName

def DownVidAdu(VidLink, VidName, path, proxy):
    #keep-alive滞留太多，需要用到session优化
    session = requests.session()
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36',
        'Host': VidLink.split('/')[2],
        'Referer': VidLink,
        'Connection': 'keep-alive',
    }
    #直到下载完成在跳出循环
    while True:
        result = NTG_base.Download(VidLink, header, path + '\\' + VidName + '.mp4', session, proxy)
        if result == True:
            break
    #返回保存路径
    return path + '\\' + VidName + '.mp4'



def start():
    #http代理
    proxy = {
        'http': 'http://127.0.0.1:10809/',
        'https': 'http://127.0.0.1:10809/',
    }
    #下载路径
    resultPath = 'C:\\Users\\NTG\\Desktop\\Youtube Downloader\\result'
    #这里填视频id，例：https://www.youtube.com/watch?v=0FRVx_c9T0c中的0FRVx_c9T0c
    VidLnk = '0FRVx_c9T0c'

    VidLink, VidName = GetVidInf(VidLnk, proxy)
    print('获取链接完成 视频名：', VidName)
    DownVidAdu(VidLink, VidName, resultPath, proxy)
    print('下载完成')


start()