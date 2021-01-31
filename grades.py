import base64
import json
from io import BytesIO

import requests
import os

session = requests.session()
grade_url="http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentScoreQuery&viewType=printScoreAll"
headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://jwc.swjtu.edu.cn",
        "Referer": "http://jwc.swjtu.edu.cn/service/login.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
headers1 = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
    
}

def ocr(source):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    params = {"image": source}
    access_token = '24.da00c8904326fa4c9753a31f9d520726.2592000.1613719265.282335-23566827'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        tmp = response.json()
        tmp = tmp['words_result']
        if len(tmp) == 0:
            return "error"
        else:
            return tmp[0]['words']


def login(username,password):
    global session
    login_url = "http://jwc.swjtu.edu.cn/vatuu/UserLoginAction"
    session.get(url="http://jwc.swjtu.edu.cn/service/login.html")
    #get verifying code
    img=session.get(url="http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG")
    source = base64.b64encode(BytesIO(img.content).read())
    verify = ocr(source)
    print (verify)
    #login
    data = {
        "username":username,
        "password":password,
        "url":"",
        "returnType":"",
        "returnUrl":"",
        "area":"",
        "ranstring":verify
    }
    doLogin=session.post(url=login_url,headers=headers,data=data)
    if '''loginStatus":"1"''' not in doLogin.text:
        print("Failed, retrying")
        return login(username,password)
    else:
        session.get(url="http://jwc.swjtu.edu.cn/vatuu/UserLoadingAction")
        return doLogin.text

def get_grades():
    global session
    username = "2020110019"
    password = "Rainrain0109."
    doLogin = login(username,password)
    print(doLogin)
    session.get(url="http://jwc.swjtu.edu.cn/vatuu/UserFramework")
    html = session.get(url=grade_url,headers=headers1)
    # print(html.text)
    html2text = open("html.html","w")
    html2text.write(str(html.text))
    html2text.close()
    os.system('wkhtmltoimage html.html out.jpg')
    






