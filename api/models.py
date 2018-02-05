from django.db import models
import datetime

class Post(models.Model):
	count = models.IntegerField(default=0)
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=15)
	url = models.CharField(max_length=200)
	site = models.CharField(max_length=20)
	item_id = models.IntegerField(default=0)
	score = models.CharField(max_length=10)
	#pub_date = models.DateTimeField(default = datetime.datetime.now())
	age = models.CharField(max_length=10, default='no date')

	def __str__(self):
		return self.title
