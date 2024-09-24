#!/media/dataj/wechat-devtools-linux/testing/myenv/bin/python
import js2py
from lxml import etree
import time
import requests, re
from tqdm import tqdm
import os, json, sys

# jianjia: this should be the place to get allow lists
def get_about_info(appid):
    # the url to click in wechat:
    # https://mp.weixin.qq.com/wxawap/waverifyinfo?action=get&appid=wx210963174dd44184
    
    # the whole request looks like this:
    # https://mp.weixin.qq.com/wxawap/waverifyinfo?
    # action=get&appid=wx210963174dd44184&uin=ODgyMTQ1NjQ0&key=daf9bdc5abc4e8d01cff299da5635d3febd66c1dfc716a5ad651e0fe5979f96694277fe11acc81e510f72fd23b652a886f1e4a7b97a466bce3f2b44a56ef3905970e6b5c9094615cb52e464a2c394a8f2477c67adcebd1bf55b50d99a31d5bbd6b0bfce223ec784127c6212d039e0fdda2af4aebd6a10ef43c978041c43ac9b7&devicetype=iMac20%2C1+OSX+OSX+13.3.1+build(22E261)&version=13080812&lang=en&nettype=WIFI&ascene=1&fontScale=100&acctmode=0&pass_ticket=z6y95WtrRgwIAUiTe9ck%2FjBlpI4idFdoVjO96mq3sOrGpbF4b1fEtYtWVbxHW3z3
    
    url = "https://mp.weixin.qq.com/wxawap/waverifyinfo?"
    # >>>>>> jianjia: key, pass_ticket, cookie should be changed timely
    # key = "daf9bdc5abc4e8d061382f314ff4e07d532ccd8d740d84a90011f21457a3b216708c3a6b5e0ec2c5c8e4e4bb1f562620b183035c905dd1b46b7b7e26194e76da104bbe37decc464442318ecbcde48e0c647c8baed9e32ffafd135819424810241b424e7658f2f08383541c8940929f5021da79a819607c736c6d39924bfb2b7a"
    key = "daf9bdc5abc4e8d0ef82c710d1b156115000df9862eaa7ae26141f04da4b5c1366b7356aae2173ba6440d58e10ed0d672203a7c8ea7203afd9db276459c10066faa9df18a4233775860e949f10f26129c9a7abb6872ea08012a6d44b0b4a32219c93f64bb3f4b4faf8fa107136b3db4b14772fe07d9d38671e330fbeed1cdd4e"
    key = "daf9bdc5abc4e8d0e6e685c244963c00a7f6dabffee5b7cf1a8896acede26a982fd50730cfb21dfd9a4e2d9d2f3aeea752042cd4279e6a84267d3617fec114845c0e4c3d3589ed4a22b1b0c7e5d6a964612cde141e21408eca763f24b157b9714d6e9c258ae7de402a0777ffe97b06d292b0c12f39aa2915915889ba9da302c0"
    # pass_ticket = "GTw4QTDR2b0ejModps8fkKmv8EW6Pa0X99+qMHdxUmW1PDh9urRWIg4yHxh5aUCU"
    # pass_ticket = "DqJ8NU2rKrncpyFrNBrgPnCazs78e+Hr2TuENNAorDO0xSzIbN9hLOqulZGNpWWs"
    pass_ticket = "okWOMDV5mjbyyyW2C2mdjRoMwXXfG2QjxQzQBYufIhFWHimbNNkcOCYpMkNJrVrg"
    params = f"action=get&appid={appid}&uin=MjA3Nzg0MDQx&key={key}&devicetype=iMac20%2C1+OSX+OSX+13.3.1+build(22E261)&version=13080812&lang=en&nettype=WIFI&ascene=1&fontScale=100&acctmode=0&pass_ticket={pass_ticket}"

    # cookie = "ua_id=eb4EDcsCOcGDKtg4AAAAAPiDoE5vBbsTqmIOTFPpM84=; mm_lang=en_US; _clck=jildfu|1|fog|0; xid=ff3791b220320bc4cc6f5ca7f0090c27; wxuin=882145644; devicetype=iMac201OSXOSX13.3.1build(22E261); version=13080813; lang=en; pass_ticket=uR5D3RKAOdPvRtcJ0kFWIeUwfn+ntRLm1wClMNfM62Elu9DBM3TxaKFUsQKjueo1; wap_sid2=COzy0aQDEnZ5X0hJMDltRXdsS2lTdnpwdUVMRURlSXNQOWtac0JOajVpaTUyZ3dyeVRZU0t2VFo0clJwbDlqNTI3aGZNY2ZJcmN3b2lmN3duZjBoODNzeHBtbFFlOGh6b1ZmRTBsRHQ3dmJPZ1NQRGd2ZDVZczVSSUFBQX5+MM6St7cGOAxAlE4="
    # cookie = "wxuin=207784041; devicetype=iMac201OSXOSX13.3.1build(22E261); version=13080813; lang=en; pass_ticket=x2XW3YhD8JHYunsVbD7vKoDkwGfixgMc3UvBLpodXJ5g93bmkYTYlnSv4+NI0VSk; wap_sid2=COmQimMSdnlfSEt3UmZQX2dvRWFkdGFuT3dpaEVpZ2hYOGo0dVJfTDhZOGlpNHprdGxiZ0twRjR1MG4tdGdDaE9Oc1lFRTlMOHo4SnBlLXYzSmUxdHRLS2YwRXVxVHlZcGJhajZQSjZYS3NtWmxsdVZXdERaNVJJQUFBfn4w9q24twY4DECUTg=="
    cookie = "wxuin=207784041; devicetype=iMac201OSXOSX13.3.1build(22E261); version=13080813; lang=en; pass_ticket=DqJ8NU2rKrncpyFrNBrgPnCazs78e+Hr2TuENNAorDO0xSzIbN9hLOqulZGNpWWs; wap_sid2=COmQimMSdnlfSExJOXFqVEFTcXhmd1pLNzk4UUtTMWZCVVJPTDhubjMzQU51dUw3cE1tb2pfTkxXRE5sZi16UlQxZHlIM0tZLU5VZ1FQaHhvZllmVkpRdm9FNXpKTlEwYmlENjFkRzVGTm1raGdzLVBsYnc0NVJJQUFBfn4w7664twY4DECUTg=="
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/6.8.0(0x16080000) MacWechat/3.8.8(0x13080812) XWEB/1216 Flue",
               'Cookie': f"{cookie}"}

    rep = requests.get(url=url, params=params, headers=headers)
    if rep.status_code == 200:
        html = rep.content.decode('utf-8')
        with open("wxapp_about/" + appid+"_info.html", "w") as f:
            f.write(html)

def get_name_from_html(filename):
    res = {'appid': filename.split("/")[-1].split("_")[0]}
    with open(filename, "r") as f:
        html = f.read()
    if html == "":
        print(f'{filename} does not contain any content')
        # os.remove(filename)
        return
    try: 
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from bs4 import BeautifulSoup
    parsed_html = BeautifulSoup(html, 'html.parser')
    scripts = (parsed_html.body.findAll('script'))
    for script in scripts:
        content = script.string
        if content:
            if 'window.cgiData' in content:
                try:
                    add = js2py.eval_js(content + ';window.cgiData;')
                    # print(add)
                    res['cgiData'] = add
                except:
                    print(f'Error processing js for {filename}')
                    # os.remove(filename)
                    return
    return res

    # the top 10 miniapps
    # appid_list = ['wx5b97b0686831c076', 
    #               'wx77af438b3505c00e',
    #               'wxaf35009675aa0b2a',
    #               'wxece3a9a4c82f58c9',
    #               'wx336dcaf6a1ecf632',
    #               'wx91d27dbf599dff74',
    #               'wxde8ac0a21135c07d',
    #               'wxd2ade0f25a874ee2',
    #               'wx43aab19a93a3a6f2',
    #               'wx40d6ea683ff7732e',
    #               'wxad3150031786d672']
    
    # the 7 miniapps in the 100 random ones
    # appid_list = [
    # "wxa1162974c4e87ccc",
    # "wx7395e8fadb4bf551",
    # "wx99ce33f04663a3b5",
    # "wx84b9d5f6d5c1880c",
    # "wx9773ea62d71dca32",
    # "wx76b2eb38228100eb",
    # "wx95e0efe85af13c86"
    # ]
    
    # the 100 random ones we select from large dataset
    # appid_file = '/media/dataj/wechat-devtools-linux/testing/auto-testing/miniapp_data/appid_file/random_100_no_error_appids.json'

    
def get_info_42w():
    # the 42w large dataset
    appid_file = '/media/data4/jianjia_data4/miniapp_data/wxapkgs-42w.json'
    
    with open(appid_file, 'r') as fp:
        package_names = json.load(fp)
    appid_list = [i.replace("-pc", "") for i in package_names if "-pc" in i]    
    
    cnt = 0
    for appid in tqdm(appid_list):
        filename = "wxapp_about/" + appid+"_info.html"
        if os.path.exists(filename):
            continue
        get_about_info(appid)
        res = get_name_from_html(filename)
        if res:
            cnt += 1
            print(f'>>>appid: {appid}')
            print(res['cgiData']['nickname'])
        else:
            print('error getting the nickname: {res}')
        # we have to wait, do not request too often
        time.sleep(30)
    print(f">>> add {cnt}")

def clean_wxapp_about_folder():
    bad_words = ["该账号"]
    files = os.listdir("wxapp_about")
    print(f'>>> cleaning wxapp_about folder: {len(files)}')
    cnt = 0
    for i in files:
        res = get_name_from_html(os.path.join('wxapp_about', i))
        if res:
            print(f'>>>appid: {i}')
            print(res['cgiData']['nickname'])
            for j in bad_words:
                if j in res['cgiData']['nickname']:
                    cnt += 1
                    print(f'>>>bad appid: {i}')
                    break
    files = os.listdir("wxapp_about")
    print(f'>>> after cleaning wxapp_about folder: {len(files)}')
    print(f'>>> bad appids: {cnt}')

if __name__=='__main__':
    # jianjia: this is running!
    # this is used to get the about info of the appid
    # how do we get the appid of a miniapp with its name and open it?
    get_info_42w()
    # clean_wxapp_about_folder()