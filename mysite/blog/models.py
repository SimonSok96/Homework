from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(created__year=2023)


class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    slug = models.SlugField(max_length=250, unique_for_date='created')
    title = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.created.year,
                                                          self.created.month,
                                                          self.created.day,
                                                          self.slug,])