import re, os
import jieba
import requests

def extract_chinese_characters(html_content):
    # Regular expression pattern to match Chinese characters
    pattern = re.compile(r'[\u4e00-\u9fff]+')
    
    # Find all Chinese characters in the HTML content
    chinese_text = ''.join(pattern.findall(html_content))
    
    return chinese_text

def segment_chinese_text(text):
    # Segment the Chinese text into words using jieba
    words = jieba.cut(text)
    
    # Join the words with a space or any other separator
    segmented_text = list(set([i for i in words]))
    
    return segmented_text

def load_keywords_from_file(file_path):
    # Load HTML content from a file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Extract Chinese characters
    chinese_text = extract_chinese_characters(html_content)

    # Segment the Chinese text into words
    segmented_text = segment_chinese_text(chinese_text)

    return segmented_text

def load_keywords_from_url(url):
    # Fetch HTML content from the specified URL
    response = requests.get(url)
    response.encoding = 'utf-8'  # Ensure the encoding is set to UTF-8
    html_content = response.text

    # Extract Chinese characters
    chinese_text = extract_chinese_characters(html_content)

    # Segment the Chinese text into words
    segmented_text = segment_chinese_text(chinese_text)

    return segmented_text

def load_keywords(input_source='src/batchKeywords/keywords.html'):
    # Determine if the input is a file path or a URL
    if os.path.isfile(input_source):
        return load_keywords_from_file(input_source)
    elif input_source.startswith(('http://', 'https://')):
        return load_keywords_from_url(input_source)
    else:
        raise ValueError("Input source must be a valid file path or URL.")
