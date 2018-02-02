from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from news.models import New_Post


def api(request):
	return render(request, 'api/api.html')


def get_page_list(request):
	context = []
	for raw in New_Post.objects.all():											
		context.append({
						'title' : raw.title,
						'author' : raw.author,
						'site' : raw.site,
						'url' : raw.url,
						'item_id' : raw.item_id,
						#'score' : ''.join([a.text for a in raw.find_all('span', class_='score')]),
						#'pub_date' : ''.join([a.text for a in raw.find_all('span', class_='age')])
						})
		
	return JsonResponse(context)
	
			
def get_site_list(request, site_name):
	context = []
	context_dict = {}
	for raw in New_Post.objects.filter(site = site_name):
		context.append({
						'title' : raw.title,
						'author' : raw.author,
						'site' : raw.site,
						'url' : raw.url,
						'item_id' : raw.item_id,
						})
	context_dict[site_name] = context
	if context_dict[site_name] == []:
		return JsonResponse({'error' : 'Does Not Exist'})
	else:
		return JsonResponse(context_dict)
