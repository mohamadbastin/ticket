from django.db import models


# Create your models here.

class Cart(models.Model):
    number = models.IntegerField()
    owner = models.CharField(max_length=1000)
