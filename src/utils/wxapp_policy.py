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
    
    # https://mp.weixin.qq.com/wxawap/waprivacyinfo?action=show&appid=wxaf35009675aa0b2a&uin=ODgyMTQ1NjQ0&key=daf9bdc5abc4e8d0c91133b91ca393cc11b7255df60a7c27b7d0ac08f679693b41c23338cd2e5341a4c3c1fb6b0e76899f988adf6d4ebbe904e84c8941483d94ae02c55cadb878edea117f10dbc8e20436e880c22690c38fa062e575cdff0ba5f657d8d4dca3b6170ca7dd14cdee9b69c63f7171ba17ea9d84a6246b399cd0ce&devicetype=UnifiedPCMac&version=f26414f0&lang=en&ascene=1&acctmode=0&pass_ticket=O8QJiRuUKx46Rkuk5LZBsakaHsChXQu2tveExbcx1zlBEzZAyaOiwO3g8bo%2BWpfu
    
    url = "https://mp.weixin.qq.com/wxawap/waprivacyinfo?"
    params =  f"action=show&appid={appid}&uin=ODgyMTQ1NjQ0&key=daf9bdc5abc4e8d0c91133b91ca393cc11b7255df60a7c27b7d0ac08f679693b41c23338cd2e5341a4c3c1fb6b0e76899f988adf6d4ebbe904e84c8941483d94ae02c55cadb878edea117f10dbc8e20436e880c22690c38fa062e575cdff0ba5f657d8d4dca3b6170ca7dd14cdee9b69c63f7171ba17ea9d84a6246b399cd0ce&devicetype=UnifiedPCMac&version=f26414f0&lang=en&ascene=1&acctmode=0&pass_ticket=O8QJiRuUKx46Rkuk5LZBsakaHsChXQu2tveExbcx1zlBEzZAyaOiwO3g8bo%2BWpfu"
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
    appid_id = 'wx66a90900db27b9ae'
    get_about_info(appid_id)