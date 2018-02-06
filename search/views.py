from django.core.serializers import serialize
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import JsonResponse

import re
import json

from search.forms import PostForm
from news.models import NewPost


def get_query_dict(raw):
	query_dict = {
				'title' : ''.join([a.text for a in raw.find_all('a', class_='storylink')]),
				'author' : ''.join([a.text for a in raw.find_all('a', class_='hnuser')]),
				'site_name' : ''.join([a.text for a in raw.find_all('span', class_='sitestr')]),
				'url' : ''.join([a.get('href') for a in raw.find_all('a', class_='storylink')]),
				'item_id' : ''.join([a.get('id') for a in raw.find_all('span', class_='score')]).replace('score_', ''),
				}

	return query_dict



def get_search(request):
	context = []
	if request.GET:
		form = PostForm(request.GET)
		if form.is_valid():
			search = form.cleaned_data['search']
			search_list = re.sub(r'^\W|$', ' ', search.lower()).split()
			for raw in NewPost.objects.all():
				if search.lower() in raw.title.lower():
					context.append(raw)
				elif search.lower() in raw.author.lower():
					context.append(raw)
				elif search.lower() in raw.site_name.lower():
					context.append(raw)
				fields_list = [raw.title, raw.author, raw.site_name]
				for field in fields_list:
					for word in search_list:
						if word in field:
							context.append(raw)
			context = dict(zip(context,context)).values()
			list(context)					
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






