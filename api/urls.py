from django.urls import path, re_path

from .views import api, get_page_list, get_site_list




urlpatterns = [
	path('', api, name = 'api'),
	path('posts/', get_page_list),
   re_path(r'posts/(?P<site_name>[$a-zA-Z0-9-.]*([.-a-zA-Z0-9\-]{0,61}[.-a-zA-Z0-9])*)', get_site_list, name = 'api_posts_site'),     
]

