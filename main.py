import time

import config
from utils.fileUtil import is_file_exist, write_file_start, write_file
from utils.httpUtil import get_request
from utils.regexUtil import get_hrefs_titles, get_date, get_words

url_prefix = config.TARGET_URL_2


def get_titles_urls(page_number):
    titles_urls = []

    url_head = url_prefix + "index"
    url_tail = ".shtml"

    for i in range(int(page_number)):
        if i == 0:
            url = url_head + url_tail
        else:
            url = url_head + "_" + str(i) + url_tail

        html = get_request(url)
        # print(html)

        for href, title in get_hrefs_titles(html):
            url = get_url(href)
            titles_urls.append((title, url))

    return titles_urls


def get_url(href):
    split = href.split("/")
    url = url_prefix + split[1] + "/" + split[2]
    return url


def get_year(date):
    split = date.split("-")
    return split[0]


if __name__ == '__main__':
    print("请输入总页数：", end="")
    p_n = input()

    data = get_titles_urls(p_n)
    print("共有 " + str(len(data)) + " 篇文章")

    count = 1
    current_year = "xxxx"
    key_words = ["文明", "发展", "安全"]
    write_file_start("files/data.csv", "Date,Title,Words,URL\n")
    for t, u in data:
        print(str(count) + "\t" + u)
        if count % 10 == 0:
            time.sleep(1)
        count = count + 1

        h = get_request(u)
        words_with_keywords = get_words(h, key_words)
        if len(words_with_keywords) == 0:
            continue

        d = get_date(h)
        year = get_year(d)
        path_to_file = "files/" + year + ".csv"
        if current_year != year:
            write_file_start(path_to_file, "Date,Title,Words,URL\n")
            current_year = year

        for word in words_with_keywords:
            # if not is_file_exist(path_to_file):
            #     write_file_start(path_to_file, "Date,Title,Words,URL\n")

            string = d + "," + t + "," + word + "," + u + "\n"
            write_file(path_to_file, string)
            write_file("files/data.csv", string)

        # if count == 10:
        #     break
