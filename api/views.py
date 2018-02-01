from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError, HttpResponse
)
#from django.template import RequestContext

from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import JsonResponse
from django.core.serializers import serialize

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib.request
import re
import json
import requests
from .models import Post


MAIN_URL = 'http://news.ycombinator.com/'

# Диапазон страниц поиска
PARSE_RANGE = 10

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


def api(request):
	return render(request, 'api/api.html')


def get_html(url):
	#request = Request(url, headers = hdr)
	#response = urlopen(request).read()
	opener = AppURLopener()
	response = opener.open(url).read()
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

def get_page_list(request):
	context = []
	soup = BeautifulSoup(get_html(MAIN_URL + '/newest'), 'lxml')
	context = get_parse(soup)
	more_link = get_link(soup)
	for page in range(PARSE_RANGE):										
		soup = BeautifulSoup(get_html(MAIN_URL + more_link), 'lxml')
		more_link = get_link(soup)
		print(more_link)
		context.extend(get_parse(soup))
	json1 = json.dumps(context, indent = 2)	

	return HttpResponse(json1)
	

		

def get_parse(soup):
	index = 0
	count = 0
	context = []
	itemlist = soup.find('table', class_ = 'itemlist')
	athing = itemlist.find_all('tr', class_='athing')
	subtext = itemlist.find_all('td', class_='subtext')
	tr_teg = itemlist.find_all('tr')
	for raw in tr_teg:
		link = raw.find('a', class_='morelink')
	more_link = link.get('href')
	for raw in athing:
		raw.insert(count, subtext[index])
		index += 1
		count += 1
		if index > len(subtext) - 1:
			index = 0
			count = 0
	for raw in athing:
		context.append(get_query_dict(raw))

	return context


def get_site_url(soup, site_name):
	itemlist = soup.find('table', class_ = 'itemlist')
	athing = itemlist.find_all('tr', class_='athing')
	for raw in athing:
		site = ''.join([a.text for a in raw.find_all('span', class_='sitestr')])
		if site_name in site:
			site_url = raw.find('span', class_ = 'sitebit comhead').a.get('href')
			return site_url
			break

def get_parse_site(site_url):
	soup = BeautifulSoup(get_html(MAIN_URL + site_url), 'lxml')
	context = get_parse(soup)
	more_link = get_link(soup)
	for page in range(PARSE_RANGE):											
		soup = BeautifulSoup(get_html(MAIN_URL + more_link), 'lxml')
		more_link = get_link(soup)
		print(more_link)
		if not more_link:
			context.extend(get_parse(soup))
			return context
		context.extend(get_parse(soup))
	
	return context


			
def get_site_list(request, site_name):
	context_dict = {}
	soup = BeautifulSoup(get_html(MAIN_URL + 'newest'), 'lxml')
	site_url = get_site_url(soup, site_name)
	if site_url != None:
		context_dict[site_name] = get_parse_site(site_url)
		json1 = json.dumps(context_dict, indent = 2)
		return HttpResponse(json1)
		
	if site_url == None: 
		more_link = get_link(soup)
		print(more_link)
		for page in range(PARSE_RANGE):											
			soup = BeautifulSoup(get_html(MAIN_URL + more_link), 'lxml')
			more_link = get_link(soup)
			print(more_link)
			site_url = get_site_url(soup, site_name)
			if site_url != None:
				context_dict[site_name] = get_parse_site(site_url)
				json1 = json.dumps(context_dict, indent = 2)
				return HttpResponse(json1)
			if site_url == None and page == PARSE_RANGE - 1:
				return HttpResponse({'error' : 'Does Not Exist'})


def handler404(request, exception, template_name='404.html'):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response    

def handler403(request, exception, template_name='403.html'):
    response = render_to_response('403.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 403
    return response    
def handler400(request, exception, template_name='400.html'):
    response = render_to_response('400.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 400
    return response    

def handler500(request, template_name='500.html'):
    return HttpResponseServerError()
