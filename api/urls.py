from django.urls import path, re_path

from .views import api, api_posts_list, api_posts_site

urlpatterns = [
	path(r'', api, name = 'api'),
	path(r'/posts/', api_posts_list),
    re_path('posts/(?P<site_name>\w+.\w+.\w+)/$', api_posts_site, name = 'api_posts_site'),     
]
