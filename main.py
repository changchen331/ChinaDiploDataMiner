import config
from utils.httpUtil import get_request
from utils.regexUtil import get_urls_titles


def get_urls(pages):
    urls_and_titles = []

    url_head = config.TARGET_URL + "index"

    for i in range(pages):
        url_tail = ".shtml"

        if i == 0:
            html = get_request(url_head + url_tail)
        else:
            html = get_request(url_head + "_" + str(i) + url_tail)

        for url_title in get_urls_titles(html):
            urls_and_titles.append(url_title)

    return urls_and_titles


# <a href="./202412/t20241204_11538482.shtml" target="_blank">王毅在外交部海南自由贸易港全球推介活动上的致辞（2024-12-04）</a>

if __name__ == '__main__':
    urls_titles = get_urls(11)

    for href, title in urls_titles:
        split = href.split("/")
        link = config.TARGET_URL + split[1] + "/" + split[2]
        print(link, title)
