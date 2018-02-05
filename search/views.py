from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import JsonResponse

import re
import json

from search.forms import PostForm
from news.models import New_Post


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
	context = []
	if request.GET:
		form = PostForm(request.GET)
		if form.is_valid():
			search = form.cleaned_data['search']
			search_list = re.sub(r'^\W|$', ' ', search.lower()).split()
			for raw in New_Post.objects.all():
				if search.lower() in raw.title.lower():
					context.append(raw)
	else:
		form = PostForm()		
	#json1 = json.dumps(context, indent = 2)
	return render_to_response('search/search.html', {
													'context' : context, 
													})


def list_filter(context):
	print(context)
	title_list = []
	for item in context:
		title_list.append(item['title'])
		if title_list.count(item['title']) > 1 :
			context.remove(item)
	print(context)		
	return context






