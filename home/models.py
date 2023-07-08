from django.db import models
from authentication.models import User

# Create your models here.
class Post(models.Model):
    title  = models.CharField(max_length = 255)
    meta_title = models.CharField(max_length = 255 , null=True,blank=True)
    author = models.CharField(max_length = 255)
    body = models.TextField()
    timeStamp = models.DateTimeField(auto_now = True)
    tags = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title + " by " + self.author


class Contact(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    subject = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name