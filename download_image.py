#-*-coding:utf-8 -*- 
import requests
import re
import threading
import os
import json
import configparser
from bs4 import BeautifulSoup

VideoDatabase={}
try:
    f = open('./temp/VideoDatabase',"r")
    VideoDatabase=json.loads(f.read())
except Exception as e:
    print('Creat VideoDatabase')
imgpath = './image/'
tmppath = './temp/'
configpath = './config/'
imgcnt=0

def getparser():
    cf = configparser.ConfigParser()
    cf.read(configpath+'config')
    Model = cf.get("config", 'Model')
    VideoType = cf.get("config", 'VideoType')
    ThreadNum = int(cf.get("config", 'ThreadNum'))
    # defaultlink = ""
    # for line in open(configpath+'default',"r"):
    #     line = line.strip()
    #     defaultlink += 
    f = open(configpath+'website', 'r')
    webtext = f.read()
    websitelink = ''
    for i,char in enumerate(webtext,0):
        websitelink += chr(ord(webtext[i])-2)
    websitelink = json.loads(websitelink)
    url = websitelink[VideoType]['link']
    PageNum = int(websitelink[VideoType]['PageNum'])
    if ThreadNum > PageNum:
        ThreadNum = PageNum
    return url,PageNum,ThreadNum

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

def download(url,name):
    r=requests.get(url , timeout = 30)
    f=open(imgpath+name,"wb")
    f.write(r.content)
    f.close()

def spider(start,end,self_url):
    global imgcnt
    global VideoDatabase
    InfoDatabase ={}
    for x in range(start,end):
        url = self_url+'&page='+str(x)
        try:
            soup,page_info=RequestWeb(url)
            links = soup.find_all('a',href=re.compile(r"view_video"))
            videoinfos = soup.find_all('img',src=re.compile(r"jpg"))
            for i in range(len(videoinfos)):
                try:
                    videopage_link=links[2*i+1]['href']
                    # print(videoinfos[i])
                    videoinfo_imglink=(str(videoinfos[i])[10:46]).replace('"','')
                    # print(videoinfo_imglink)
                    videotitle=(str(videoinfos[i])[55:str(videoinfos[i]).find('width')-2])
                    videotitle=videotitle.replace(' ','').replace('"','').replace('/','').replace('<','').replace('>','').replace('*','').replace('?','')
                    videoID=videoinfo_imglink[26:videoinfo_imglink.find('.jpg')]
                    # print(videoID)
                    download(videoinfo_imglink,videotitle+'##'+videoID+'##'+'.jpg')
                    InfoDatabase['index'] = imgcnt
                    InfoDatabase['videotitle'] = videotitle
                    InfoDatabase['videopage_link'] = str(videopage_link)
                    VideoDatabase[str(videoID)] = InfoDatabase
                    InfoDatabase ={}

                    imgcnt = imgcnt+1
                    if imgcnt%1000 == 0:
                        saveDatabase(VideoDatabase)
                        print('had download',imgcnt,'images')

                except Exception as e:
                    print('page='+str(x)+' i='+str(i)+'  ',e)
        except Exception as e:
            print(e)
    saveDatabase(VideoDatabase)

def runspider(url,PageNum,ThreadNum):
    perthread=int(PageNum/ThreadNum)
    for i in range(0,ThreadNum):
        t = threading.Thread(target=spider,args=(perthread*i+1,perthread*(1+i)+1,url,))
        t.start()

def saveDatabase(Database):
    f = open('./temp/VideoDatabase',"w+")
    f.write(str(json.dumps(Database)))

def main():
    mkdir(imgpath)
    mkdir(tmppath)
    url,PageNum,ThreadNum = getparser()
    print('PageNum:',PageNum,' ThreadNum:',ThreadNum,' VideoNum:',PageNum*20)
    runspider(url,PageNum,ThreadNum)

if __name__ == '__main__':
    main()