from django.db import models


YEARS = [(x, x) for x in range(1950, 2026)]


class InfoBase(models.Model):
    title = models.CharField(max_length=150, verbose_name="назва")
    original_title = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="оригінальна назва",
    )
    release_date = models.PositiveSmallIntegerField(
        verbose_name="дата виходу", choices=YEARS, default=2020
    )
    description = models.TextField(max_length=10000, verbose_name="опис")

    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        ordering = ("title",)


class Film(InfoBase):
    # directors = ArrayField(
    #     models.CharField(max_length=100), default=list, verbose_name="режисер"
    # )
    # actors = ArrayField(
    #     models.CharField(max_length=100), default=list, verbose_name="актори"
    # )
    image = models.ImageField(
        upload_to="archives/films", blank=True, null=True
    )


class Anime(InfoBase):
    studio = models.CharField(max_length=100, verbose_name="студія")
    episodes = models.PositiveSmallIntegerField(
        verbose_name="кількість епізодів"
    )
    image = models.ImageField(
        upload_to="archives/anime", blank=True, null=True
    )


class Game(InfoBase):
    developer = models.CharField(max_length=100, verbose_name="розробник")
    # platforms = ArrayField(
    #     models.CharField(max_length=100),
    #     default=list,
    #     verbose_name="платформи",
    # )
    image = models.ImageField(
        upload_to="archives/games", blank=True, null=True
    )
