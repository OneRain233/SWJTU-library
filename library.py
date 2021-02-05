import time
import requests
import json
import datetime
import base64
from io import BytesIO

url = "http://zuowei.lib.swjtu.edu.cn/api.php/spaces_old?area={}&day={}&startTime={}&endTime=22:30"
arealist = [24, 10, 16, 15, 22, 7, 6, 21, 11, 14, 16, 12, 8, 23, 9, 19]
arealist.sort()
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
nowtime = time.strftime("%H:%M", time.localtime())


def ocr(source):
    # 验证码位数
    cont = 4
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    params = {"image": source}
    access_token = ''
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()

def findseat():
    choose = input("选择一个黄道吉日：1--今天； 2--明天\n")
    if choose == "1":
        for i in arealist:
            freelist = []
            urlnew = url.format(i, today, nowtime)
            tip = "now:{}".format(i)
            req = requests.get(urlnew)
            reqjson = json.loads(req.text)
            zwlist = reqjson['data']['list']
            total = 0
            free = 0
            for j in zwlist:
                total = total + 1
                if "\u7a7a\u95f2" in j['status_name']:
                    free = free + 1
                    res = "{}---{}是空闲的".format(j['area_name'], j['no'])
                    print(res)
                else:
                    res = "{}---{}被占了".format(j['area_name'], j['no'])
                    # print("\033[1;31;40m")
                    print("\033[1;31;40m" + res + "\033[0m")
                    # print ("\033[0m")
            print("\033[1;30;42m" + "{}扫描完成,共有{}座位,还有{}空闲".format(i, total, free) + "\033[0m")
    elif choose == "2":
        for i in arealist:
            freelist = []
            urlnew = url.format(i, tomorrow, "7:30")
            tip = "now:{}".format(i)
            req = requests.get(urlnew)
            reqjson = json.loads(req.text)
            zwlist = reqjson['data']['list']
            total = 0
            free = 0
            for j in zwlist:
                total = total + 1
                if "\u7a7a\u95f2" in j['status_name']:
                    free = free + 1
                    res = "{}---{}是空闲的".format(j['area_name'], j['no'])
                    print(res)
                elif "\u5df2\u9884\u7ea6" in j['status_name']:
                    res = "{}---{}被占了".format(j['area_name'], j['no'])
                    print("\033[1;31;40m" + res + "\033[0m")
            print("\033[1;30;42m" + "{}扫描完成,共有{}座位,还有{}空闲".format(i, total, free) + "\033[0m")
    else:
        print("煞笔！！！！！！让你选1 2")


def login(username, password):
    verify = ""
    session = requests.session()
    origeurl = "https://zuowei.lib.swjtu.edu.cn/home/web/seat/area/1"
    loginurl = "https://zuowei.lib.swjtu.edu.cn/api.php/login"
    verifyurl = "https://zuowei.lib.swjtu.edu.cn/api.php/check"
    header = {
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
        "Origin": 'https://zuowei.lib.swjtu.edu.cn',
        "Sec-Fetch-Site": "same - origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
    }
    session.get(origeurl, headers=header)
    img = session.get(verifyurl, headers=header)
    source = base64.b64encode(BytesIO(img.content).read())
    print("GET verifycode")
    verify = ocr(source)
    tmp = verify['words_result']
    verify = tmp[0]['words']
    print(verify)

    data = {
        'username': username,
        'password': password,
        'verify': verify
    }
    proxies = {
        "http": "http://127.0.0.1:8080"
    }
    dologin = session.post(loginurl, data, headers=header)
    if '''"status":1''' not in dologin.text:
        return login(username,password)
    else:
        print("login successfully")
        ans = dologin.text
        return ans
        print("login successfully")


if __name__ == '__main__':
    mode = input("Please select a mode:\n1.Find free seats\n2.Login\n")
    if mode == "1":
        findseat()
    elif mode == "2":
        username = ""
        password = ""
        res = login(username, password)
        print(res)
        information = json.loads(res)
        information = information['data']
        accesstoken = information['_hash_']['access_token']
        userid = information['_hash_']['userid']
        print("Accesstoken:" + accesstoken)
        print("Userid:" + userid)
    elif mode == "3":
        raw = '''{"status":1,"msg":"\u767b\u9646\u6210\u529f","data":{"list":{"id":"0000375303","card":"3194085161","name":"\u5218\u54f2","idCard":null,"gender":1,"birthday":"","joinTime":"2020-09-17 17:45:06","wallet":".0000","saving":".0000","fillScore":0,"totalFillScore":0,"consumeScore":0,"totalConsumeScore":0,"role":null,"roleName":"\u672c\u79d1\u751f","dept":null,"deptName":"\u897f\u5357\u4ea4\u5927-\u5229\u5179\u5b66\u9662","subDept":null,"subDeptName":null,"tel":null,"mobile":"13326294741","email":null,"qq":null,"status":1,"weixin":null,"hw_update_flag":0,"skedb_update_flag":1,"ROW_NUMBER":"1","renegeinfo":null},"_hash_":{"userid":"0000375303","access_token":"3ea94d5488609ec99567287b03e5423f","expire":"2021-01-20 18:32:03"}}}'''
        information = json.loads(raw)
        information = information['data']
        accesstoken = information['_hash_']['access_token']
        userid = information['_hash_']['userid']
        print("Accesstoken:" + accesstoken)
        print("Userid:" + userid)
