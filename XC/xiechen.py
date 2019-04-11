import requests
from  bs4 import BeautifulSoup
import random
import time
import os

placeArray = [{"poiID":10547264, "districtId": 171, "resourceId":137657, "name":"井冈山"}]

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Host": "you.ctrip.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

url = "http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView"
data = {'poiID': 0, 'districtId': 171, 'districtEName': 'Jinggangshan', 'pagenow': 1, 'order': 3.0, 'star': 0.0,
        'tourist': 0.0, 'resourceId': 137657, 'resourcetype': 2}

class XCCrawler:

    def __init__(self):
        self.get_result()

    def get_result(self):
        for place in placeArray:
            #主数据
            mc=[]
            #评分数据
            star=[]
            #评论时间
            date=[]
            self.districtId = place['districtId']
            self.poiID = place['poiID']
            self.resourceId = place['resourceId']
            placeName = place['name']
            self.getPageCount()
            if self.allCount > 1:
                for i in range(1,2):
                    sleepTime = random.uniform(1, 5)
                    html=requests.post(url,headers=headers,data=data)
                    html.encoding="utf-8"
                    soup=BeautifulSoup(html.content)
                    block=soup.find_all(class_="comment_single")
                    for j in block:
                        text=j.find(class_="heightbox")
                        try :
                            start=j.find(class_="sblockline")
                            st=start.text
                            date.append(j.find(class_="time_line").text)
                        except AttributeError:
                            st=""
                        mc.append(text.text)
                        star.append(st)
                    time.sleep(round(sleepTime, 2))

                self.createDataFile(mc,star,placeName)

    '''
        获取总页码
    '''
    def getPageCount(self):
        data['districtId'] = self.districtId;
        data['poiID'] = self.poiID;
        data['resourceId'] = self.resourceId;
        html = requests.post(url, headers=headers, data=data)
        html.encoding = "utf-8"
        soup = BeautifulSoup(html.content)
        allCount = 0
        if soup.find(class_="numpage").text != None:
            allCount = int(soup.find(class_="numpage").text)
        self.allCount = allCount

    '''
        创建数据文件
    '''
    def createDataFile(self,mc,star,placeName):
        path = os.path.abspath('.') + r"/data/";
        # 如果不存在则创建相应目录
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(path + placeName + '.txt', 'a', encoding='utf-8')
        for i in range(len(mc)):
            file.write(mc[i] + "\n   评分：" + star[i] + "\n")
            print(mc[i]);
        file.close();
        print("数据抓取成功===> " + placeName);

