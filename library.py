import time
import requests
import json
import datetime

url = "http://zuowei.lib.swjtu.edu.cn/api.php/spaces_old?area={}&day={}&startTime={}&endTime=22:30"
arealist = [44,45,46,47,24,10,16,15,39,22,31,40,7,6,38,21,11,36,42,32,34,37,41,35,14,16,12,8,33,23,9,19,18]
arealist.sort()
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
nowtime = time.strftime("%H:%M", time.localtime())

def findseat():
    choose = input("选择一个黄道吉日：1--今天； 2--明天")
    if choose == "1":
        for i in arealist:
            urlnew = url.format(i,today,nowtime)
            tip = "now:{}".format(i)
            req = requests.get(urlnew)
            reqjson = json.loads(req.text)
            zwlist = reqjson['data']['list']
            for j in zwlist:
                if "\u7a7a\u95f2" in j['status_name']:
                    res = "{} {}是空闲的".format(j['area_name'],j['no'])
                    print(res)
    elif choose == "2":
        for i in arealist:
            urlnew = url.format(i,tomorrow,"7:30")
            tip = "now:{}".format(i)
            req = requests.get(urlnew)
            reqjson = json.loads(req.text)
            zwlist = reqjson['data']['list']
            for j in zwlist:
                if "\u7a7a\u95f2" in j['status_name']:
                    res = "{}{}是空闲的".format(j['area_name'],j['no'])
                    print(res)
    else:
        print("煞笔！！！！！！让你选1 2")


findseat()
