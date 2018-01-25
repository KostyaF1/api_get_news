from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils import timezone
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import re
import json

from api.forms import PostForm


MAIN_URL = 'ycombinator.com'

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


def get_search(request):
	context = []
	if request.GET:
		form = PostForm(request.GET)
		if form.is_valid():
			search = form.cleaned_data['search']
			search_list = re.sub(r'^\W|$', ' ', search.lower()).split()
			context = parse(search_list)	
		
	else:
		form = PostForm()	

	json1 = json.dumps(context, indent = 2)		

	return render_to_response('search/search.html', {
													'form': form, 
													'json1': json1, 
													'context':context, 
													})


def parse(search_list):
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
			title = ''.join([a.text for a in raw.find_all('a', class_='storylink')])
			author = ''.join([a.text for a in raw.find_all('a', class_='hnuser')])
			site = ''.join([a.text for a in raw.find_all('span', class_='sitestr')])
			fields_list = [title, site, author]
			for field in fields_list:
				for search in search_list:
					if search in field.lower():
						url = ''.join([a.get('href') for a in raw.find_all('a', class_='storylink')])
						score = ''.join([a.text for a in raw.find_all('span', class_='score')])
						item_id = ''.join([a.get('id') for a in raw.find_all('span', class_='score')]).replace('score_', '')
						pub_date = ''.join([a.text for a in raw.find_all('span', class_='age')])
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




