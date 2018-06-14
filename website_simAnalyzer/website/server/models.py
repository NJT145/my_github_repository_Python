from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField, ArrayField


class UserGroup(models.Model):
    mail = models.EmailField(max_length=100, unique= True)
    password = models.CharField(max_length=100)
    info = JSONField(blank=True, null=True)
    #prefered_books = JSONField(blank=True, null=True)
    #similar_books = JSONField(blank=True, null=True)

class Books(models.Model):
    name = models.CharField(max_length=500, unique=True)
    topic_titles = ArrayField(ArrayField(models.CharField(max_length=100)))
