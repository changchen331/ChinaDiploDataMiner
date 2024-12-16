import re

from bs4 import BeautifulSoup


def is_un_info(html):
    pattern = r'联合国'
    return re.search(pattern, html)


def get_urls_titles(html):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 查找所有具有target="_blank"属性的<a>标签
    links = []
    for link in soup.find_all('a', href=True, target='_blank'):
        href = link['href']

        if href.startswith('.') and not href.startswith('..'):
            title = link.get_text(strip=True)  # 提取链接的标题，并去除首尾空格
            links.append((href, title))

    return links


def get_words(html, keywords):
    # 提取所有<p>标签的内容
    paragraphs = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)

    # 存储包含关键词的句子
    words_with_keywords = []

    # 遍历每个段落，检查是否包含关键词
    for paragraph in paragraphs:
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

    return words_with_keywords
