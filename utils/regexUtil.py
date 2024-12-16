import re
from datetime import datetime

from bs4 import BeautifulSoup


def is_un_info(html):
    pattern = r'联合国'
    match = re.search(pattern, html)

    return match is not None


def get_hrefs_titles(html):
    # <a href="./202412/t20241204_11538482.shtml" target="_blank">王毅在外交部海南自由贸易港全球推介活动上的致辞（2024-12-04）</a>

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 查找所有具有target="_blank"属性的<a>标签
    anchors = []
    for link in soup.find_all('a', href=True, target='_blank'):
        href = link['href']

        if href.startswith('.') and not href.startswith('..'):
            title = link.get_text(strip=True)  # 提取链接的标题，并去除首尾空格
            anchors.append((href, title))

    return anchors


def get_date(html):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 找到class为"time"的<p>标签，然后找到其内部的<span>标签
    time_p = soup.find('p', class_='time')
    # 在<p>标签内找到所有的<span>标签
    spans = time_p.find_all('span')

    # 定义时间格式的正则表达式
    time_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}')
    time_info = "9999-12-31 23:59"
    for span in spans:
        # 检查<span>标签的文本内容是否匹配时间格式
        if time_pattern.match(span.text.strip()):
            # 提取时间信息
            time_info = span.text.strip()
            break
    # 提取<span>标签中的文本，即时间信息
    # time_info = time_span.text

    # 将时间字符串转换为datetime对象（可选，但有助于后续处理）
    time_obj = datetime.strptime(time_info, '%Y-%m-%d %H:%M')
    # 仅保留年月日部分，并格式化为字符串
    date_only = time_obj.strftime('%Y-%m-%d')

    return date_only


def get_words(html, keywords):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')
    # 找到所有的<p>标签
    paragraphs = soup.find_all('p')

    # 存储包含关键词的句子
    words_with_keywords = []

    # 若 match = False，则只搜索提及“联合国”的文章
    match = False
    # 若 match = True，则搜索所有文章
    # match = True
    # 遍历每个段落，检查是否包含关键词
    for paragraph in paragraphs:
        paragraph_text = paragraph.get_text()
        match = match or is_un_info(paragraph_text)

        # 去除段落中的HTML标签
        clean_paragraph = re.sub(r'<.*?>', '', paragraph_text)

        # 分割成句子（这里简单地使用句号、问号、感叹号作为句子的分隔符）
        sentences = re.split(r'[。！？]', clean_paragraph)

        # 去除空句子和只包含空格的句子
        sentences = [s.strip() for s in sentences if s.strip()]

        # 检查每个句子是否包含关键词
        for sentence in sentences:
            if any(keyword in sentence for keyword in keywords):
                words_with_keywords.append(sentence)

    if match:
        # print("包含'联合国'")
        return words_with_keywords
    else:
        # print("无关")
        return []
