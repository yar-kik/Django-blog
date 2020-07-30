from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)

    # phone = PhoneField(blank=True, help_text='Enter phone number')
    # phone = PhoneNumberField()

    def __str__(self):
        return f'Profile for user {self.user.username}'


# Create your models here.

class Contact(models.Model):
    """Проміжна модель для збережння додаткової інформації (дата і час створення).
    Відтворює форму ManyToManyField. Також можна і надалі використовувати стандартну модель
    User без її модифікації"""
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set',  # Хто підписався
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set',  # На кого підписалися
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Динамічно додаємо поля following в модель User
User.add_to_class('following', models.ManyToManyField('self', through=Contact,
                                                      related_name='followers',
                                                      symmetrical=False))
