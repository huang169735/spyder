import requests
from  bs4 import BeautifulSoup
import DB.sql as sql
import random
import time
import os
import CONFIG
import proxy
import traceback

'''
placeArray = {
        "井冈山":{"poiID":10547264, "districtId": 171, "resourceId":137657},
        "黄洋界":{"poiID":79958, "districtId": 171, "resourceId":17854},
        "茨坪景区":{"poiID":78619, "districtId": 100054, "resourceId":12131},
        "井冈山革命博物馆":{"poiID":79956, "districtId": 171, "resourceId":17852},
        "杜鹃山":{"poiID":78626, "districtId": 171, "resourceId":12165},
        "龙潭瀑布群":{"poiID":78623, "districtId": 171, "resourceId":12139},
        "井冈山烈士陵园":{"poiID":79955, "districtId": 171, "resourceId":17851}
}
'''
placeArray = {
        "毛泽东故居":{"poiID":79888, "districtId": 346, "resourceId":17772},
        "毛泽东纪念馆":{"poiID":87313, "districtId": 346, "resourceId":63036},
        "韶山":{"poiID":10547448, "districtId": 346, "resourceId":138673},
        "滴水洞":{"poiID":79887, "districtId": 346, "resourceId":17771},
        "毛泽东铜像":{"poiID":87314, "districtId": 346, "resourceId":63037},
        "毛泽东纪念园":{"poiID":10774161, "districtId": 346, "resourceId":1408751}
}


url = "http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView"
data = {'poiID': 0, 'districtId': 171, 'districtEName': 'Jinggangshan', 'pagenow': 1, 'order': 3.0, 'star': 0.0,
        'tourist': 0.0, 'resourceId': 137657, 'resourcetype': 2}

class XCCrawler:

    def __init__(self,placeData):
        self.proxys = []
        for pd in placeData:
            try:
                place = placeArray[pd['name']]
                place['id'] = pd['id']
            except Exception:
                print("更新景点不含"+pd['name'])
        #self.get_allResult()
        resultErrorList = sql.queryErrorLog("xc")
        if len(resultErrorList)>0:
           self.updateErrorData(resultErrorList)

    def get_allResult(self):
        for placeName in placeArray:
            place = placeArray[placeName]
            self.districtId = place['districtId']
            self.poiID = place['poiID']
            self.resourceId = place['resourceId']
            self.id = place['id']
            self.getPageCount()
            if self.allCount > 1:
                paNo = 0
                pid = ""
                updateCount = 0
                for i in range(1,self.allCount):
                    sleepTime = random.uniform(1, 5)
                    data['pagenow'] = i
                    soup = self.build_post(data,self.id)
                    if soup != None:
                        updateCount = self.saveData(sleepTime, soup, updateCount, i, self.id)
                        paNo = i
                        pid = self.id
                        print("携程数据抓取成功===> " + placeName+" 第"+str(paNo)+"页")
                sql.saveLog(updateCount,"携程",pid,paNo)
                #self.createDataFile(mainData,placeName)
        #更新错误记录
        resultErrorList = sql.queryErrorLog("xc")
        if len(resultErrorList)>0:
            self.updateErrorData(resultErrorList)
        sql.close()

    def updateErrorData(self,updateDataList):
        self.proxys = proxy.getProxys()
        updateCount = 0
        count = 0
        for row in updateDataList:
            ID = row[0]
            parms = row[1]
            pid = row[2]
            parmsDict = eval(parms)
            soup = self.build_post(parmsDict,pid)
            if soup != None:
                sleepTime = random.uniform(1, 5)
                self.saveData(sleepTime,soup,updateCount,parmsDict['pagenow'],pid)
                sql.updateErrorLog(ID)
                count = count + 1
        resultErrorList = sql.queryErrorLog("xc")
        print("更新携程错误记录"+str(count)+"条，剩余错误"+str(len(resultErrorList))+"条")
        if len(resultErrorList)>0:
            self.updateErrorData(resultErrorList)
        else:
            sql.deleteErroeLog()

    def saveData(self, sleepTime, soup, updateCount, pageNo, pid):
        # 主数据
        mainData = []
        block = soup.find_all(class_="comment_single")
        for j in block:
            result = {}
            text = j.find(class_="heightbox")
            id = j.find(id="usefultodo")['data-id']
            name = j.find(class_="ellipsis").text
            date = j.find(class_="time_line").text
            try:
                start = j.find(class_="sblockline")
                st = start.text
            except AttributeError:
                st = ""
            result['content'] = text.text
            result['starText'] = st
            result['name'] = name
            result['date'] = date
            result['id'] = id
            result['pageNo'] = pageNo
            mainData.append(result)
            updateCount += 1
        time.sleep(round(sleepTime, 2))
        sql.saveData(pid, mainData)
        return updateCount

    '''
        获取总页码
    '''
    def getPageCount(self):
        data['districtId'] = self.districtId;
        data['poiID'] = self.poiID;
        data['resourceId'] = self.resourceId;
        soup = self.build_post(data,self.id)
        allCount = 0
        if soup != None:
            if soup.find(class_="numpage") != None and soup.find(class_="numpage").text:
                allCount = int(soup.find(class_="numpage").text)
                self.allCount = allCount
        else:
            self.getPageCount()


    def build_post(self,requestData, id):
        head = CONFIG.headers
        head['Host'] = "you.ctrip.com"
        proxyIp = self.randomIP()
        proxys = proxy.buildProxy(proxyIp['ip'],proxyIp['port'])
        try:
            html = requests.post(url, headers=head, data=requestData, timeout=5, proxies=proxys)
            if 200 == html.status_code:
                html.encoding = "utf-8"
                return BeautifulSoup(html.content, "lxml")
            else:
                print("请求错误 >>> 页面状态：" + str(html.status_code) + "\n" + html.text)
                sql.saveErrorLog("xc", data, id)
                sql.updateScore(proxy);
                return None
        except Exception as e:
            #traceback.print_exc()
            print("请求错误 >>> "+str(proxyIp)+" >> "+str(requestData))
            sql.saveErrorLog("xc", data, id)
            sql.updateScore(proxyIp);
            return None


    def randomIP(self):
        if len(self.proxys) == 0:
            self.proxys = proxy.getProxys()
        return random.choice(self.proxys)

    '''
        创建数据文件
    '''
    def createDataFile(self,md,placeName):
        path = os.path.abspath('.') + r"/data/";
        # 如果不存在则创建相应目录
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(path + placeName + '.txt', 'a', encoding='utf-8')
        for i in range(len(md)):
            file.write("id >> "+md[i]['id']+"  name >> "+md[i]['name']+"  时间 >> "+md[i]['date']+"\n"+md[i]['content'] + "\n   评分：" + md[i]['starText'] + "\n")
        file.close();
        print("数据抓取成功===> " + placeName);



