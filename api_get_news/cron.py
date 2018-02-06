from django.shortcuts import get_object_or_404, render, render_to_response
from django.conf import settings

from bs4 import BeautifulSoup
import urllib.request

from news.models import NewPost

MAIN_URL = 'http://news.ycombinator.com/'


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"

def get_html(url):
    opener = AppURLopener()
    response = opener.open(url).read()
    return response


def get_parse():
    soup = BeautifulSoup(get_html(MAIN_URL + '/newest'), 'lxml')
    index = 0
    count = 0
    context = []
    itemlist = soup.find('table', class_ = 'itemlist')
    athing = itemlist.find_all('tr', class_='athing')
    subtext = itemlist.find_all('td', class_='subtext')
    for raw in athing:
        raw.insert(count, subtext[index])
        index += 1
        count += 1
        if index > len(subtext) - 1:
            index = 0
            count = 0       
    for raw in athing:
        title = ''.join([a.text for a in raw.find_all('a', class_='storylink')])
        author = ''.join([a.text for a in raw.find_all('a', class_='hnuser')])
        site_name = ''.join([a.text for a in raw.find_all('span', class_='sitestr')])
        url = ''.join([a.get('href') for a in raw.find_all('a', class_='storylink')])
        item_id = ''.join([a.get('id') for a in raw.find_all('span', class_='score')]).replace('score_', '')

        NewPost.objects.get_or_create(
                                        title = title,
                                        author = author,
                                        site_name = site_name,
                                        url = url,
                                        item_id = item_id,
                                        )
    
    print('ok')
            