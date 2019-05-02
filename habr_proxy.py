import re
import urllib
from bs4 import BeautifulSoup
from django.http import HttpResponse

import replacer


HOST = 'https://habr.com/'


def change_anchors(html_page, new_host):
    """ Change host in href attribute for all <a> tags on HTML page

    :param html_page: HTML page
    :param new_host: new host address
    :return: changed HTML page
    """
    soup = BeautifulSoup(html_page, 'html.parser')
    for link in soup.findAll(
            'a', attrs={'href': re.compile("^{}".format(HOST))}):
        link['href'] = link.get('href').replace(HOST, new_host)
    return str(soup)


def habr_proxy(request, path):
    """ Method that calls when user trying to get HTML page from web browser

    :param request: django HttpRequest
    :param path: url path
    :return: django HttpResponse
    """
    print(request)
    with urllib.request.urlopen('{}{}'.format(HOST, path)) as response:
        html_page = response.read()
    html_page = change_anchors(
        html_page, 'http://{}/'.format(request.get_host()))
    html_page = replacer.add_char_to_html(html_page)
    return HttpResponse(html_page)
