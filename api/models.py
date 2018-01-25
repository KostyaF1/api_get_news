from django.db import models

class Post(models.Model):
	count = models.IntegerField(default=0)
	title = models.CharField(max_length=200)
	author = models.CharField(max_length=200)
	url = models.CharField(max_length=200)
	site = models.CharField(max_length=200)
	#pub_date = models.DateTimeField(default = timezone.now())

	def __str__(self):
		return self.title
