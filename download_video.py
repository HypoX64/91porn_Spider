#-*-coding:utf-8 -*- 
from bs4 import BeautifulSoup
import re
import requests
import json
import configparser
import os


def getparser():
    cf = configparser.ConfigParser()
    cf.read('./config/config')
    Model = cf.get("config", 'Model')
    return Model

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)  
        print (path+' 创建成功')
        return True
    else:
        return False

def RequestWeb(url):
    headers = {'Accept-Language':'zh-CN,zh;q=0.9',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
            }
    r = requests.get(url, headers = headers, timeout = 30)
    page_info = r.text
    soup = BeautifulSoup(page_info, 'html.parser')
    return soup,page_info

def download(url,name,path):
    r = requests.get(url, stream = True, timeout = 30)
    f = open(path+name, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)

def writedata(data):
    f = open('./video/videolist.txt',"a+")
    f.write(str(data)+'\n')

def main():
    mkdir('./video/')
    f=open('./temp/VideoDatabase',"r")
    VideoDatabase=json.loads(f.readlines()[0])
    Model = getparser()
    imgnames = os.listdir('./choose_video_want_to_download/')
    for imgname in imgnames:
        try:
            id=imgname[imgname.find('##')+2:imgname.find('.jpg')-2]
            videopage_link=VideoDatabase[id]['videopage_link']
            soup,page_info = RequestWeb(videopage_link)
            videolinks = soup.find_all('source',src=re.compile(r"mp4"))
            videolink = str(videolinks[0]['src'])
            if Model == 'view_select_down':
                writedata(videolink)
                download(videolink,VideoDatabase[id]['videotitle']+'.mp4','./video/')
            else:
                writedata(videolink)
            print(VideoDatabase[id]['videotitle'],'succeed!')
        except Exception as e:
            print(VideoDatabase[id]['videotitle'],'failed! ',e)

if __name__ == '__main__':
    main()