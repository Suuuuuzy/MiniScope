# this is used to search into the miniapps on Android with keywords
from dynamic.pgc import CrawlWXMicroWebView
from pathlib import Path
from batchKeywords.get_keywords import load_keywords

config_path = Path.cwd() / 'config' / 'crawler' / 'batch_config.toml'
crawler = CrawlWXMicroWebView.from_config_file(config_path)
# crawler.search_into_with_app_name("外卖")
# crawler.search_into_with_app_name("语音转文字")
# crawler.search_into_with_app_name("披萨")
name_list = load_keywords()

with open("src/batchSearchedWords.txt") as f:
    content = f.read()
searchedWords = content.split("\n")

name_list = [i for i in name_list if i not in searchedWords]
print(f"searching {len(name_list)} keywords")
crawler.search_into_with_app_name(name_list)