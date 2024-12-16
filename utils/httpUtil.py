import requests

import config


def get_request(url):
    response = requests.get(url, headers=config.HEADERS)
    response.encoding = response.apparent_encoding
    html = response.text
    # print(html)

    return html
