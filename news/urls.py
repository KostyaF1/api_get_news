from django.urls import path, re_path

from .views import NewsList, get_site_posts


urlpatterns = [
	path('', NewsList.as_view(), name = 'news_list'),
	re_path(r'^detail/(?P<site_name>([$a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})', get_site_posts, name = 'news_detail'),
]