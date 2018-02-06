from django.contrib import admin

from .models import NewPost

class NewPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'site_name')
	list_filter = ['site_name']
	search_fields = ['title']


admin.site.register(NewPost, NewPostAdmin)
