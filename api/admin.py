from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author' ,'url', 'site')


admin.site.register(Post, PostAdmin)
