import requests
import json
import random
import DB.sql as sql
import CONFIG

def getProxys():
    r = requests.get('http://127.0.0.1:8000/?types=0&count=500&country=国内')
    ip_ports = json.loads(r.text)
    ipList = random.sample(ip_ports, len(ip_ports))
    proxies=[]
    for ip_port in ipList:
        ip = ip_port[0]
        port = ip_port[1]
        ipInfo = {
            "ip":ip,
            "port":port
        }
        proxies.append(ipInfo)
    return proxies

def buildProxy(ip,port):
    return {
        'http': 'http://%s:%s' % (ip, port),
        'https': 'http://%s:%s' % (ip, port)
    }

if __name__ == '__main__':
    proxyIp = random.choice(getProxys())
    proxy = buildProxy(proxyIp['ip'],proxyIp['port'])
    print(proxy)
    try:
        head = CONFIG.headers
        #13head['Host'] = "you.ctrip.com"
        data = {'poiID': 10547264, 'districtId': 171, 'districtEName': 'Jinggangshan', 'pagenow': 1, 'order': 3.0, 'star': 0.0,
                'tourist': 0.0, 'resourceId': 137657, 'resourcetype': 2}
        r = requests.post('http://you.ctrip.com', timeout=30, headers=head, proxies=proxy)
        r.encoding = 'utf-8'
        print(r.status_code)
        if r.ok:
            #print(r.text)
            print("测试通过")
    except Exception as e:
        print(e)
        sql.updateScore(proxyIp)

