from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from archives.models import InfoBase, Film


class Article(models.Model):
    CATEGORIES = [
        ('F', "Фільми"),
        ('G', "Ігри"),
        ('A', 'Аніме')
    ]
    """
    Клас для збереження статей.
    """
    category = models.CharField(max_length=1, choices=CATEGORIES, default='', verbose_name='категорія')
    related_item = models.ForeignKey(InfoBase, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, verbose_name='назва статті')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    text = models.TextField(max_length=15000, verbose_name='текст')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата створення')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='дата редагування')
    slug = models.SlugField(max_length=100)
    objects = models.Manager
    users_like = models.ManyToManyField(User, related_name='articles_liked', blank=True)
    users_bookmark = models.ManyToManyField(User, related_name='articles_bookmarked', blank=True)

    class Meta:
        ordering = ('-date_created',)
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', args=[self.slug])


class Comment(models.Model):
    """Клас для збереження коментарів конкретної статті.
    Атрибути:
        article - стаття до якої прикриплений коментар;
        name - модель користувача-автора коментаря;
        body - текст коментаря;
        created - дата створення;
        updated - дата редагування;
        active - чи активний коментар;"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=2000, verbose_name='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    path = ArrayField(models.IntegerField(blank=True, null=True), default=list)
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply',
                                 null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.article}'

    def save(self):
        if self.id is None:
            super().save()
            self.path.append(self.id)
        super().save()

    def get_offset(self):
        level = len(self.path)
        if level > 5:
            level = 5
        return level

    def get_col(self):
        level = len(self.path)
        if level > 5:
            level = 5
        return 24 - level