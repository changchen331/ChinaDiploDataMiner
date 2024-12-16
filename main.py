import config
from utils.fileUtil import is_file_exist, write_file_start, write_file
from utils.httpUtil import get_request
from utils.regexUtil import get_hrefs_titles, get_date, is_un_info, get_words


def get_dates_titles_urls(page_number):
    dates_titles_urls = []

    url_head = config.TARGET_URL + "index"
    url_tail = ".shtml"

    for i in range(page_number):
        if i == 0:
            url = url_head + url_tail
        else:
            url = url_head + "_" + str(i) + url_tail

        html = get_request(url)
        for href, title in get_hrefs_titles(html):
            date = get_date(title)
            url = get_url(href)
            dates_titles_urls.append((date, title, url))

    return dates_titles_urls


def get_url(href):
    split = href.split("/")
    url = config.TARGET_URL + split[1] + "/" + split[2]
    return url


def get_year(date):
    split = date.split("-")
    return split[0]


if __name__ == '__main__':
    data = get_dates_titles_urls(11)

    # for date, title, url in data:
    #     print(date + "\t" + title + "\t" + url)

    key_words = ["文明", "发展", "安全"]
    for d, t, u in data:
        h = get_request(u)
        if is_un_info(h):
            words_with_keywords = get_words(h, key_words)

            if len(words_with_keywords) == 0:
                continue

            write_file_start("files/data.csv", "Date,Title,Words,URL\n")
            year = get_year(d)
            path_to_file = "files/" + year + ".csv"
            for word in words_with_keywords:
                if not is_file_exist(path_to_file):
                    write_file_start(path_to_file, "Date,Title,Words,URL\n")

                string = d + "," + t + "," + word + "," + u + "\n"
                write_file(path_to_file, string)
                write_file("files/data.csv", string)
