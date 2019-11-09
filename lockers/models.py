from django.db import models


# Create your models here.

class Cart(models.Model):
    number = models.CharField(max_length=1000)
    owner = models.CharField(max_length=1000)
