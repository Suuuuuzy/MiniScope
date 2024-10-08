import os, re, json
import subprocess
from tqdm import tqdm
import multiprocessing as mp
from loguru import logger
# import logging
# logger_main = logging.getLogger(__name__)

# logging.basicConfig(
#     filename='check_navi.log',
#     level=logging.DEBUG,
#     format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
# )
from miniapp import output_json

project_path = "/media/dataj/miniapp_data/wxapkgs-42w-unpacked"

def check_with_doublex(all_project_lists):
    logger.remove()
    logger.add('check_navi.log')
    for pkg in tqdm(all_project_lists):    
        pkg_path = os.path.join(project_path, pkg)
        bind_json_file = os.path.join(pkg_path, "bind_methods_navi.json")
        if not os.path.exists(bind_json_file):
            try:
                output_json(pkg_path, pkg_path, True)
                logger.info(f"Sucess generating bind_methods_navi.json for {pkg_path}")
            except:
                logger.error(f"Error generating bind_methods_navi.json for {pkg_path}")
                
                
def get_pkg_list():
    all_project_lists = [i for i in os.listdir(project_path) if i.startswith('wx') and len(i)==21]
    print(len(all_project_lists))

    # not with wxpay template
    with open("/media/dataj/wechat-devtools-linux/testing/auto-testing/miniapp_data/utils/check_wxpay_list.log") as f:
        content = f.read()
        pattern = r'wx[a-zA-Z0-9]{16}-pc'
        # Find all matches in the sample text
        matches = re.findall(pattern, content)
        matches = set(matches)

    all_project_lists = [i for i in all_project_lists if i not in matches]
    print(len(all_project_lists))

    # not checked with doublex
    with open("check_navi.log") as f:
        content = f.read()
        pattern = r'wx[a-zA-Z0-9]{16}-pc'
        # Find all matches in the sample text
        matches = re.findall(pattern, content)
        matches = set(matches)

    all_project_lists = [i for i in all_project_lists if i not in matches]
    print(len(all_project_lists))
    
    # not checked with regular expression
    with open("check_navi_with_reg.log") as f:
        content = f.read()
        pattern = r'wx[a-zA-Z0-9]{16}-pc'
        # Find all matches in the sample text
        matches = re.findall(pattern, content)
        matches = set(matches)

    all_project_lists = [i for i in all_project_lists if i not in matches]
    print(len(all_project_lists))
    

    return all_project_lists

def get_cmrf_pattern():
    # cmrf 
    ROUTE_API = [
        'wx.switchTab',
        'wx.reLaunch',
        'wx.redirectTo',
        'wx.navigateTo',
        'wx.navigateToSync',
        'wx.navigateBack'
    ]
    # cmrf 
    NAVIGATE_API = [
        'wx.navigateToMiniProgram',
        'wx.navigateBackMiniProgram',
        'wx.exitMiniProgram'
    ]
    
    combined_list = ROUTE_API + NAVIGATE_API
    combined_list = [i.replace("wx.", "") for i in combined_list]
    # Join the list elements into a single string separated by the '|' operator
    pattern_string = '|'.join(combined_list)
    pattern = rf'({pattern_string})'    
    return pattern

def check_with_reg_expression(all_project_lists):
    logger.remove()
    logger.add('check_navi_with_reg.log')
    
    navi_list = set()
    pattern = get_cmrf_pattern()
    for pkg in all_project_lists:
        pkg_path = os.path.join(project_path, pkg)
        output_file = os.path.join(pkg_path, "navi.txt")
        if os.path.exists(output_file):
            continue
        navi_dic = {}
        app_json_file = os.path.join(pkg_path, "app.json")
        # print(app_json_file)
        if os.path.exists(app_json_file):
            try:
                with open(app_json_file) as f:
                    app_json = json.load(f)
            except:
                continue
            if "pages" in app_json:
                for page in app_json["pages"]:
                    js_file = os.path.join(pkg_path, page+".js")
                    if not os.path.exists(js_file):
                        continue
                    with open(js_file) as f:
                        content = f.read()
                    matches = re.findall(pattern, content)
                    if len(matches)>0:
                        navi_dic[page] = matches
                        navi_list.add(pkg)
        if navi_dic!={}:
            with open(output_file, "w") as f:
                json.dump(navi_dic, f, indent=2)
            logger.info(f"{pkg_path} uses navigation APIs")
        else:
            logger.info(f"No navigation APIs in {pkg_path}")
    # return navi_list
    
    
def main():
    
    # all_project_lists = get_pkg_list()
    # package_names = [i for i in os.listdir(project_path) if i.startswith('wx') and len(i)==21]
    package_names = get_pkg_list()
    # package_names = package_names[:100]
    # all_project_lists = ["wx62f7a94211bc34c5-pc"]
    
    processes = 128
    batch_size = (len(package_names) + processes - 1) // processes
    batched_package_names = [package_names[i:i+batch_size] for i in range(0, len(package_names), batch_size)]
    with mp.Pool(processes=processes) as pool:
        pool.map(check_with_reg_expression, batched_package_names)

    # check_with_reg_expression(all_project_lists)
    # check_with_doublex(all_project_lists)

if __name__ == '__main__':       
    main()