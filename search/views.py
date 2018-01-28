from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import JsonResponse
from django.utils import timezone

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import json

from search.forms import PostForm


MAIN_URL = 'ycombinator.com/'

# Диапазон страниц поиска
PARSE_RANGE = 25       

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


def get_link(soup):
	itemlist = soup.find('table', class_ = 'itemlist')
	tr_teg = itemlist.find_all('tr')
	for raw in tr_teg:
		link = raw.find('a', class_='morelink')
	more_link = link.get('href')
	return more_link

def get_query_dict(raw):
	query_dict = {
				'title' : ''.join([a.text for a in raw.find_all('a', class_='storylink')]),
				'author' : ''.join([a.text for a in raw.find_all('a', class_='hnuser')]),
				'site' : ''.join([a.text for a in raw.find_all('span', class_='sitestr')]),
				'url' : ''.join([a.get('href') for a in raw.find_all('a', class_='storylink')]),
				'score' : ''.join([a.text for a in raw.find_all('span', class_='score')]),
				'item_id' : ''.join([a.get('id') for a in raw.find_all('span', class_='score')]).replace('score_', ''),
				'pub_date' : ''.join([a.text for a in raw.find_all('span', class_='age')])
				}

	return query_dict



def get_search(request):
	try:
		context = []
		if request.GET:
			form = PostForm(request.GET)
			if form.is_valid():
				search = form.cleaned_data['search']
				search_list = re.sub(r'^\W|$', ' ', search.lower()).split()
				soup = BeautifulSoup(get_html(MAIN_URL + '/newest'), 'lxml')
				context = get_parse(soup, search_list)
				more_link = get_link(soup)
				for page in range(PARSE_RANGE):											
					soup = BeautifulSoup(get_html(MAIN_URL + more_link), 'lxml')
					more_link = get_link(soup)
					print(more_link)
					context.extend(get_parse(soup, search_list))
	
				if context == []:
					return render_to_response('search/search.html', { 'error' : 'Does Not Exist'})
		else:
			form = PostForm()
		context = list_filter(context)		
		json1 = json.dumps(context, indent = 2)
		return render_to_response('search/search.html', {
														'form' : form, 
														'json1' : json1, 
														'context' : context, 
														})
	except:
		return JsonResponse({'status' : 403, 'error' : 'Forbidden'})

def get_parse(soup, search_list):
	index = 0
	count = 0
	context = []
	itemlist = soup.find('table', class_ = 'itemlist')
	athing = itemlist.find_all('tr', class_ = 'athing')
	subtext = itemlist.find_all('td', class_ = 'subtext')
	tr_teg = itemlist.find_all('tr')
	for raw in tr_teg:
		link = raw.find('a', class_ = 'morelink')
	more_link = link.get('href')
	for raw in athing:
		raw.insert(count, subtext[index])
		index += 1
		count += 1
		if index > len(subtext) - 1:
			index = 0
			count = 0
	for raw in athing:
		title = ''.join([a.text for a in raw.find_all('a', class_ = 'storylink')])
		author = ''.join([a.text for a in raw.find_all('a', class_ = 'hnuser')])
		site = ''.join([a.text for a in raw.find_all('span', class_ = 'sitestr')])
		fields_list = [title, site, author]
		for search in search_list:
			for field in fields_list:
				if search in field.lower():
					url = ''.join([a.get('href') for a in raw.find_all('a', class_ = 'storylink')])
					score = ''.join([a.text for a in raw.find_all('span', class_ = 'score')])
					item_id = ''.join([a.get('id') for a in raw.find_all('span', class_ = 'score')]).replace('score_', '')
					pub_date = ''.join([a.text for a in raw.find_all('span', class_ = 'age')])
					context.append({
									'title' : title,
									'author' : author,
									'site' : site,
									'url' : url,
									'score': score,
									'item_id': item_id,
									'pub_date' : pub_date
									})
	return context

def list_filter(context):
	print(context)
	title_list = []
	for item in context:
		title_list.append(item['title'])
		if title_list.count(item['title']) > 1 :
			context.remove(item)
	print(context)		
	return context






