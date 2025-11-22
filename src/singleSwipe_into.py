#!/Users/jianjia/Documents/projects/mini-app/MiniScope/myenv/bin/python

# this is used to search into the miniapps on Android with keywords
from dynamic.pgc import CrawlWXMicroWebView
from pathlib import Path

config_path = Path.cwd() / 'config' / 'crawler' / 'batch_config.toml'
crawler = CrawlWXMicroWebView.from_config_file(config_path)
# crawler.search_into_with_app_name("外卖")
# crawler.search_into_with_app_name("语音转文字")
# crawler.search_into_with_app_name("披萨")
crawler.swipe_into()
