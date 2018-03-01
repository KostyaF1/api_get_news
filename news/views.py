from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import JsonResponse
from django.core.serializers import serialize

from .models import NewPost


class NewsList(ListView):

    model = NewPost
    paginate_by = 30

    def get_queryset(self):
        #context = super().get_context_data(**kwargs)
        news = NewPost.objects.all()
        paginator = Paginator(news, 30) 
        return news

def get_site_posts(request, site_name):
	context = []
	paginate_by = 30
	for raw in NewPost.objects.filter(site_name = site_name):
		context.append({
						'title' : raw.title,
						'author' : raw.author,
						'site_name' : raw.site_name,
						'url' : raw.url,
						'item_id' : raw.item_id,
						'id' : raw.id
						})
	paginator = Paginator(context, 30)
	return render_to_response('news/newpost_detail.html', {
													'context' : context
													})	


