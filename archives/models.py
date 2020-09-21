from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from taggit.managers import TaggableManager

from articles.tagging import TaggedWhatever, TaggedGenres

YEARS = [(x, x) for x in range(1950, 2026)]


class Film(models.Model):
    title = models.CharField(max_length=150)
    original_title = models.CharField(max_length=150, blank=True, default='')
    release_date = models.PositiveSmallIntegerField(verbose_name='Дата виходу', choices=YEARS, default=2020)
    genres = TaggableManager(through=TaggedGenres)
    tags = TaggableManager(through=TaggedWhatever)
    directors = ArrayField(models.CharField(max_length=100), default=list)
    actors = ArrayField(models.CharField(max_length=100), default=list)
    description = models.TextField(max_length=10000)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Anime(models.Model):
    title = models.CharField(max_length=150)
    original_title = models.CharField(max_length=150, blank=True, default='')
    release_date = models.PositiveSmallIntegerField(verbose_name='Дата виходу', validators=[MinValueValidator(1900),
                                                                                            MaxValueValidator(2025)])
    genres = TaggableManager(through=TaggedGenres)
    tags = TaggableManager(through=TaggedWhatever)
    studio = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    episodes = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Game(models.Model):
    title = models.CharField(max_length=150)
    original_title = models.CharField(max_length=150, blank=True, default='')
    release_date = models.PositiveSmallIntegerField(verbose_name='Дата виходу', validators=[MinValueValidator(1900),
                                                                                            MaxValueValidator(2025)])
    genres = TaggableManager(through=TaggedGenres)
    tags = TaggableManager(through=TaggedWhatever)
    developer = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    platforms = ArrayField(models.CharField(max_length=100), default=list)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)