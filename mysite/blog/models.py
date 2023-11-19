from django.db import models
from django.contrib.auth.models import User



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(created__year=2023)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
