from django.db import models
import datetime

class NewPost(models.Model):
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=15)
	site_name = models.CharField(max_length=20, default = 'none.com') 
	url = models.CharField(max_length=200)
	item_id = models.IntegerField(default=0)

	def __str__(self):
		return self.title