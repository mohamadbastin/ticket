from django.db import models


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField()
    text = models.CharField(max_length=10000, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    video = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title


class Sponsor(models.Model):
    name = models.CharField(max_length=128)
    picture = models.ImageField()
    text = models.CharField(max_length=10000, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

