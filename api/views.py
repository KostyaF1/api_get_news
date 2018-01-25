from django.http import  HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render_to_response, render
from django.core.serializers import serialize
from django.utils import timezone

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
from lxml.html.soupparser import fromstring
import re
import json
from .models import Post


MAIN_URL = 'ycombinator.com/'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def get_html(url):
	request = Request('https://news.' + url, headers=hdr)
	response = urlopen(request).read()
	
	return response

'''
def get_url(url):
	resp = requests.get('https://news.' + url + '/newest')
	soup = BeautifulSoup(resp.content, 'lxml')	
	table = soup.find('table', class_ = 'itemlist')
	tr = table.find_all('tr')
	for i in tr:
		a = i.find('a', class_='morelink')
	url = a.get('href')
	return url
'''

def api_posts_list(request):
	index = 0
	count = 0
	context = []
	for page in range(1, 20):
		soup = BeautifulSoup(get_html(MAIN_URL + '?p=%d' % page), 'lxml')
		table = soup.find('table', class_ = 'itemlist')
		tr_teg = table.find_all('tr', class_='athing')
		td_teg = table.find_all('td', class_='subtext')
		for raw in tr_teg:
			raw.insert(count, td_teg[index])
			index += 1
			count += 1
			if index > len(td_teg) - 1:
				index = 0
				count = 0
		for raw in tr_teg:
			context.append({
							'title' : ''.join([a.text for a in raw.find_all('a', class_='storylink')]),
							'author' : ''.join([a.text for a in raw.find_all('a', class_='hnuser')]),
							'site' : ''.join([a.text for a in raw.find_all('span', class_='sitestr')]),
							'url' : ''.join([a.get('href') for a in raw.find_all('a', class_='storylink')]),
							'score' : ''.join([a.text for a in raw.find_all('span', class_='score')]),
							'item_id' : ''.join([a.get('id') for a in raw.find_all('span', class_='score')]).replace('score_', ''),
							'pub_date' : ''.join([a.text for a in raw.find_all('span', class_='age')])
							})
	if context == []:
		return HttpResponse('Does not exist')
	else:
		json1 = json.dumps(context, indent = 2)		

	return HttpResponse(json1)


def api_posts_site(request, site_name):
	d = {}
	index = 0
	count = 0
	context = []
	#more_posts = get_url(MAIN_URL)
	for page in range(1, 20):
		soup = BeautifulSoup(get_html(MAIN_URL + '?p=%d' % page), 'lxml')
		table = soup.find('table', class_ = 'itemlist')
		tr_teg = table.find_all('tr', class_='athing')
		td_teg = table.find_all('td', class_='subtext')
		for raw in tr_teg:
			raw.insert(count, td_teg[index])
			index += 1
			count += 1
			if index > len(td_teg) - 1:
				index = 0
				count = 0
		for raw in tr_teg:
			site = ''.join([a.text for a in raw.find_all('span', class_='sitestr')])
			if site_name in site:
				title = ''.join([a.text for a in raw.find_all('a', class_='storylink')])
				author = ''.join([a.text for a in raw.find_all('a', class_='hnuser')])
				url = ''.join([a.get('href') for a in raw.find_all('a', class_='storylink')])
				score = ''.join([a.text for a in raw.find_all('span', class_='score')])
				item_id = ''.join([a.get('id') for a in raw.find_all('span', class_='score')]).replace('score_', '')
				pub_date = ''.join([a.text for a in raw.find_all('span', class_='age')])
				context.append({
								'title' : title,
								'author' : author,
								'url' : url,
								'score' : score,
								'item_id' : item_id,
								'pub_date' : pub_date
								})
	if context == []:
		 return HttpResponse('Does not exist')
	else:
		d[site_name] = context
		json1 = json.dumps(d, indent = 2)

	return HttpResponse(json1)


def api(request):
	return render(request, 'api/api.html')


