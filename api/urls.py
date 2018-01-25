from django.urls import path, re_path

from .views import api, api_posts_list, api_posts_site

urlpatterns = [
	path('', api, name = 'api'),
	path('posts/', api_posts_list),
    re_path(r'posts/(?P<site_name>\w+.\w+.\w+)/$', api_posts_site, name = 'api_posts_site'),     
]
