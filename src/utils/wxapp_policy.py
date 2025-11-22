import js2py
from lxml import etree
import time
import requests, re

def get_policy_info(appid):
    # get this from proxyman when sending request: 
    # https://mp.weixin.qq.com/wxawap/waprivacyinfo?action=show&appid=wxaf35009675aa0b2a&uin=ODgyMTQ1NjQ0&key=daf9bdc5abc4e8d0594a5af0bf0a05cebd8a3c1de30f628c6d3dc5dfe232a5bae3ba489c989eaf8a340dc1c917e944ac9c5d7c5f4de101c884311fd5b9e54431be5fb8bceea46467a0355f46af7142973c2e4afc5a18c7f3e417999b911fdd224f98719554f6afca3962b294920c2f8286a4c573894145e37db22a7ad6604c94&devicetype=UnifiedPCMac&version=f26414f0&lang=en&ascene=1&acctmode=0&pass_ticket=p0Zc4H6ALVITACtJc34tvwDjqxDx3K7UvBnyCGkw4oQ2rWM32iCHnZcWdwd5iFgB
    
    url = "https://mp.weixin.qq.com/wxawap/waprivacyinfo?"
    params =  f"action=show&appid={appid}&&uin=ODgyMTQ1NjQ0&key=daf9bdc5abc4e8d0594a5af0bf0a05cebd8a3c1de30f628c6d3dc5dfe232a5bae3ba489c989eaf8a340dc1c917e944ac9c5d7c5f4de101c884311fd5b9e54431be5fb8bceea46467a0355f46af7142973c2e4afc5a18c7f3e417999b911fdd224f98719554f6afca3962b294920c2f8286a4c573894145e37db22a7ad6604c94&devicetype=UnifiedPCMac&version=f26414f0&lang=en&ascene=1&acctmode=0&pass_ticket=p0Zc4H6ALVITACtJc34tvwDjqxDx3K7UvBnyCGkw4oQ2rWM32iCHnZcWdwd5iFgB"
    headers={ "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv)" } #微信两个校验值
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) MacWechat/3.8.7(0x13080712) UnifiedPCMacWechat(0xf26414f0) XWEB/16962 Flue"
    }
    # cookies = {
    #     "session_id": "1234567890"
    # }
    pattern = r"request_domain: \{([^\}]+)\}"
    rep = requests.get(url=url, params=params, headers=headers)
    if rep.status_code == 200:
        html = rep.content.decode('utf-8')
        with open("out/policy/" + appid+"_info.html", "w") as f:
            f.write(html)

if __name__=='__main__':
    # input: appid, output: out/policy/appid_info.html
    appid_id = 'wxaf35009675aa0b2a'
    get_policy_info(appid_id)