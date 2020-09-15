from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify


class Image(models.Model):
    """
    Клас для збереження зображення, доданих в закладки.
    Атрибути:
        user - вказує користувача, який додає зображення в закладки;
        title - заголовок картинки;
        slug - коротке найменування картинки, для створення семантичних URL'ів;
        url - посилання на оригінальну картинку;
        image - файл зображення;
        description - необов'язкове поле опису;
        created - дата створення об'єкту в базі даних;
        users_like - поле, для користувачів, яким сподобалося зображення;
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now=True, db_index=True)
    # За допомогою related_name можна звертатися до зв'язаних объектів
    # у вигляді image.users_like.all() або із об'єкта користувача user
    # як user.images_liked.all()
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """При збереженні, якщо зображення не має slug'а,
        він буде сформований автоматично із заголовка"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
