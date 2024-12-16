import requests


def get_request(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    html = response.text
    return html
