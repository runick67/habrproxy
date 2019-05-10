import re
from bs4.element import Comment


WORD_LENGTH = 6
ADDING_CHAR = '™'
REG_EXP = r'\b\w{{{}}}\b'.format(WORD_LENGTH)


def has_matches(text):
    """ Returns if text has 6-char word

    :param text: text to search
    :return: if text has matches
    """
    if len(text) < WORD_LENGTH:
        return False
    return re.search(REG_EXP, text, re.IGNORECASE)


def replace(text):
    """ Adds '™' char to all 6-char words in string

    :param text: text fo search
    :return: text with '™' char
    """
    for index, match in enumerate(
            re.finditer(REG_EXP, text, re.IGNORECASE)):
        insert_index = match.end() + index * len(ADDING_CHAR)
        text = text[:insert_index] + ADDING_CHAR + text[insert_index:]
    return text


def tag_visible(element):
    """ Returns if tag is visible on web page

    :param element: element for check
    :return: if tag is visible on web page
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta',
                               '[document]'] or isinstance(element, Comment):
        return False
    return True


def add_char_to_html(soup):
    """ Adds '™' char ant the end of 6-char words in the web page

    :param soup: BeautifulSoup
    """
    for res in filter(tag_visible, soup.findAll(text=True)):
        if has_matches(res):
            res.replace_with(replace(res))
