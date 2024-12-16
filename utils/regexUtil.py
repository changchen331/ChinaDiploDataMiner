import re

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


def get_date(text):
    # 使用正则表达式匹配括号内的时间信息
    pattern = r'(\d{4}-\d{2}-\d{2})'  # 匹配 yyyy-mm-dd 格式的时间
    matches = re.findall(pattern, text)

    # 获取最后匹配的时间（如果只有一个匹配，matches[-1] 也适用）
    if matches:
        date = matches[-1]  # 获取最后一个匹配项
    else:
        date = "时间信息匹配失败"

    return date


def get_words(html, keywords):
    # 提取所有<p>标签的内容
    paragraphs = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)

    # 存储包含关键词的句子
    words_with_keywords = []

    match = True
    # 遍历每个段落，检查是否包含关键词
    for paragraph in paragraphs:
        match = match or is_un_info(paragraph)

        # 去除段落中的HTML标签
        clean_paragraph = re.sub(r'<.*?>', '', paragraph)

        # 分割成句子（这里简单地使用句号、问号、感叹号作为句子的分隔符）
        sentences = re.split(r'[。！？]', clean_paragraph)

        # 去除空句子和只包含空格的句子
        sentences = [s.strip() for s in sentences if s.strip()]

        # 检查每个句子是否包含关键词
        for sentence in sentences:
            if any(keyword in sentence for keyword in keywords):
                words_with_keywords.append(sentence)

    if match:
        print("包含'联合国'")
        return words_with_keywords
    else:
        print("无关")
        return []
