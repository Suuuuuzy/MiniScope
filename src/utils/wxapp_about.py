import js2py
from lxml import etree
import time
import requests, re

def traverse(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            traverse(value)  # 递归遍历属性值
            if isinstance(value, int) and "time" in key:
                obj[key] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))
    elif isinstance(obj, list):
        for item in obj:
            traverse(item)  # 递归遍历列表项        


# 选取想要的域名元素
def Get_MiddleStr(content,startStr,endStr): #获取中间字符串的⼀个通⽤函数
	startIndex = content.index(startStr)
	if startIndex>=0:
		startIndex += len(startStr)
		endIndex = content.index(endStr)
	return content[startIndex:endIndex].split(',')

# jianjia: this should be the place to get allow lists
def get_about_info(appid):
    
    # https://mp.weixin.qq.com/wxawap/waverifyinfo?
    # action=get&appid=wx210963174dd44184&uin=ODgyMTQ1NjQ0&key=daf9bdc5abc4e8d01cff299da5635d3febd66c1dfc716a5ad651e0fe5979f96694277fe11acc81e510f72fd23b652a886f1e4a7b97a466bce3f2b44a56ef3905970e6b5c9094615cb52e464a2c394a8f2477c67adcebd1bf55b50d99a31d5bbd6b0bfce223ec784127c6212d039e0fdda2af4aebd6a10ef43c978041c43ac9b7&devicetype=iMac20%2C1+OSX+OSX+13.3.1+build(22E261)&version=13080812&lang=en&nettype=WIFI&ascene=1&fontScale=100&acctmode=0&pass_ticket=z6y95WtrRgwIAUiTe9ck%2FjBlpI4idFdoVjO96mq3sOrGpbF4b1fEtYtWVbxHW3z3
    
    # url = "https://mp.weixin.qq.com/wxawap/waverifyinfo?action=get&appid={}".format(appid)
    url = "https://mp.weixin.qq.com/wxawap/waverifyinfo?"
    params =  f"action=get&appid={appid}&uin=ODgyMTQ1NjQ0&key=daf9bdc5abc4e8d01cff299da5635d3febd66c1dfc716a5ad651e0fe5979f96694277fe11acc81e510f72fd23b652a886f1e4a7b97a466bce3f2b44a56ef3905970e6b5c9094615cb52e464a2c394a8f2477c67adcebd1bf55b50d99a31d5bbd6b0bfce223ec784127c6212d039e0fdda2af4aebd6a10ef43c978041c43ac9b7&devicetype=iMac20%2C1+OSX+OSX+13.3.1+build(22E261)&version=13080812&lang=en&nettype=WIFI&ascene=1&fontScale=100&acctmode=0&pass_ticket=z6y95WtrRgwIAUiTe9ck%2FjBlpI4idFdoVjO96mq3sOrGpbF4b1fEtYtWVbxHW3z3"
    headers={ "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv)" } #微信两个校验值
    # headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    # }
    # cookies = {
    #     "session_id": "1234567890"
    # }
    pattern = r"request_domain: \{([^\}]+)\}"
    rep = requests.get(url=url, params=params, headers=headers)
    if rep.status_code == 200:
        html = rep.content.decode('utf-8')
        # content = html
        # matches = re.findall(pattern, content)
        # if len(matches)>0:
        #     source_name = matches[0]
        #     source_name = source_name.strip()
        #     source_name = source_name.replace(" ", "")
        #     domains = [i.replace("\"", "").replace(",", "") for i in source_name.split("\n") if "\"" in i]
        with open(appid+"_info.json", "w") as f:
            f.write(html)

if __name__=='__main__':
    appid_id = 'wxe5f52902cf4de896'
    get_about_info(appid_id)