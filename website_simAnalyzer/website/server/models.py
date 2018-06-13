from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField


class User(AbstractUser):
    prefered_books = JSONField()
    similar_books = JSONField()

    def __str__(self):
        return self.email

    def get_preferedBooks(self):
        return self.prefered_books

    def set_preferedBooks(self):
        return self.prefered_books

    def get_similarBooks(self):
        return self.similar_books


class Books(models.Model):
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=500)
    writer = models.CharField(max_length=500)
    lang = models.CharField(max_length=20)
    topic_titles = models.CharField(max_length=1000)
    borrowing_no = models.FloatField(default=0.0)

