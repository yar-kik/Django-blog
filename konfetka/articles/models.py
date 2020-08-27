from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Article(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=10000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=50, db_index=True)
    objects = models.Manager
    tags = TaggableManager()
    users_like = models.ManyToManyField(User, related_name='articles_liked', blank=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', args=[self.slug])


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.article}'

