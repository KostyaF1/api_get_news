from django.urls import path, re_path

from .views import get_search


urlpatterns = [
    re_path('^$', get_search, name='post_search'),
    ]