from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from news.models import NewPost


def api(request):
	return render(request, 'api/api.html')


def get_page_list(request):
	context = []
	for raw in NewPost.objects.all():											
		context.append({
						'title' : raw.title,
						'author' : raw.author,
						'site_name' : raw.site_name,
						'url' : raw.url,
						'item_id' : raw.item_id,
						})
		
	return JsonResponse(context, safe = False)
	
			
def get_site_list(request, site_name):
	context = []
	context_dict = {}
	for raw in NewPost.objects.filter(site_name = site_name):
		context.append({
						'title' : raw.title,
						'author' : raw.author,
						'site_name' : raw.site_name,
						'url' : raw.url,
						'item_id' : raw.item_id,
						})
	context_dict[site_name] = context
	if context_dict[site_name] == []:
		return JsonResponse({'error' : 'Does Not Exist'})
	else:
		return JsonResponse(context_dict)
