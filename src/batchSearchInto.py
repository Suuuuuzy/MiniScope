# this is used to search into the miniapps on Android with keywords
from dynamic.pgc import CrawlWXMicroWebView
from pathlib import Path

config_path = Path.cwd() / 'config' / 'crawler' / 'batch_config.toml'
crawler = CrawlWXMicroWebView.from_config_file(config_path)
# crawler.search_into_with_app_name("外卖")
# crawler.search_into_with_app_name("语音转文字")
# crawler.search_into_with_app_name("披萨")
name_list = ["家长会打卡", "天天练商城", "雅正乐器"]
crawler.search_into_with_app_name(name_list)
