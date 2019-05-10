import re
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse

import replacer


HOST = 'https://habr.com/'


def change_tag_links(soup, tag, tag_attr, new_host):
    """ Change host for tag on the HTML page

    :param soup: BeautifulSoup
    :param tag: tag name
    :param tag_attr: tag attribute
    :param new_host: new host address
    """
    for link in soup.findAll(
            tag, attrs={tag_attr: re.compile("^{}".format(HOST))}):
        link[tag_attr] = link.get(tag_attr).replace(HOST, new_host)


def change_links(soup, new_host):
    """ Change host for all <a> and <use> tags on the HTML page

    :param soup: BeautifulSoup
    :param new_host: new host address
    :return: changed HTML page
    """
    change_tag_links(soup, 'a', 'href', new_host)
    change_tag_links(soup, 'use', 'xlink:href', new_host)


def habr_proxy(request, path):
    """ Method that calls when user trying to get HTML page from web browser

    :param request: django HttpRequest
    :param path: url path
    :return: django HttpResponse
    """
    url = '{}{}'.format(HOST, path)
    try:
        habr_response = requests.get(url)
    except Exception as e:
        return HttpResponse(e, status=404)
    content_type = habr_response.headers['Content-Type']
    status_code = habr_response.status_code
    if 'text/html' in content_type:
        habr_response = BeautifulSoup(habr_response.text, 'html5lib')
        change_links(habr_response, 'http://{}/'.format(request.get_host()))
        replacer.add_char_to_html(habr_response)
        habr_response = str(habr_response)
    return HttpResponse(habr_response, status=status_code,
                        content_type=content_type)
