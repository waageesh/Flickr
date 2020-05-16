from django.db import models

# Create your models here.

class UploadImages(models.Model):
	image = models.ImageField()
	group_id = models.CharField(max_length = 50)
	group_name = models.CharField(max_length = 50)
	image_id = models.IntegerField()
	user = models.CharField(max_length=50)
	# def __str__(self):
	# 	return self.group_id