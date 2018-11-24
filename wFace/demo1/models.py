from django.db import models

# Create your models here.
class User(models.Model):
	userName = models.CharField(max_length=100)
	email = models.CharField(max_length=100)	
	address = models.CharField(max_length=100)	
	encoded = models.CharField(max_length=1024)		