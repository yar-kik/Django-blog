from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFill

from archives.models import InfoBase, Film


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='publish')


class Article(models.Model):
    CATEGORIES = [
        ('film', "Фільми"),
        ('game', "Ігри"),
        ('anime', 'Аніме')
    ]
    STATUS_CHOICES = [
        ('draft', 'Чернетка'),
        ('moderation', 'На модерації'),
        ('publish', 'Опублікований')
    ]
    """
    Клас для збереження статей.
    """
    category = models.CharField(max_length=16, choices=CATEGORIES, default='film', verbose_name='категорія')
    related_item = models.ForeignKey(InfoBase, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name='назва статті')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="автор")
    text = models.TextField(max_length=20000, verbose_name='текст')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата створення')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='дата редагування')
    slug = models.SlugField(max_length=100)
    objects = models.Manager()
    published = PublishedManager()
    users_like = models.ManyToManyField(User, related_name='articles_liked', blank=True)
    users_bookmark = models.ManyToManyField(User, related_name='articles_bookmarked', blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='draft', verbose_name='статус')
    large_picture = ProcessedImageField(upload_to='articles/large/', blank=True,
                                        default='default/large-article-picture.jpg',
                                        verbose_name='картинка для ПК', processors=[ResizeToFill(1280, 720)],
                                        format='JPEG')
    medium_picture = ImageSpecField(source='large_picture', processors=[ResizeToFill(640, 360)], format='JPEG')
    small_picture = ImageSpecField(source='large_picture', processors=[ResizeToFill(320, 180)], format='JPEG')

    class Meta:
        ordering = ('-date_created',)
        permissions = [('can_moderate_article', 'Може одобрювати статті'),
                       ('can_draft_article', 'Може створювати чернетку статті')]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', args=[self.slug])


class Comment(models.Model):
    """Клас коментарів конкретної статті"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=2000, verbose_name='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    path = ArrayField(models.IntegerField(blank=True, null=True), default=list)
    reply_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply',
                                 null=True, blank=True)
    users_like = models.ManyToManyField(User, blank=True, related_name='comments_liked')

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
