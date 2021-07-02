import os

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from phonenumber_field.modelfields import PhoneNumberField
from pilkit.processors import ResizeToFill


class Profile(models.Model):
    SEX = [("", "Не обрано"), ("M", "Чоловіча"), ("F", "Жіноча")]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="дата народження"
    )
    sex = models.CharField(
        max_length=1, choices=SEX, blank=True, verbose_name="стать"
    )
    photo = ProcessedImageField(
        upload_to="user/avatar/%Y/%m/%d/",
        blank=True,
        default="default/profile-picture.png",
        verbose_name="фото профілю",
        processors=[ResizeToFill(200, 200)],
        format="JPEG",
    )
    phone = PhoneNumberField(
        blank=True, null=True, unique=True, verbose_name="номер телефону"
    )

    def __str__(self):
        return f"Profile for user {self.user.username}"


class Contact(models.Model):
    """Проміжна модель для збережння додаткової інформації (дата і час створення).
    Відтворює форму ManyToManyField. Також можна і надалі використовувати стандартну модель
    User без її модифікації"""

    user_from = models.ForeignKey(
        "auth.User",
        related_name="rel_from_set",  # Хто підписався
        on_delete=models.CASCADE,
    )
    user_to = models.ForeignKey(
        "auth.User",
        related_name="rel_to_set",  # На кого підписалися
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# Динамічно додаємо поля following в модель User
User.add_to_class(
    "following",
    models.ManyToManyField(
        "self", through=Contact, related_name="followers", symmetrical=False
    ),
)
User._meta.get_field("email")._unique = True


# @receiver(models.signals.post_delete, sender=Profile)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     """
#     Deletes file from filesystem
#     when corresponding `MediaFile` object is deleted.
#     """
#     if instance.photo:
#         if os.path.isfile(instance.photo.path):
#             os.remove(instance.photo.path)
#
#
# @receiver(models.signals.pre_save, sender=Profile)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     """
#     Deletes old file from filesystem
#     when corresponding `MediaFile` object is updated
#     with new file.
#     """
#     if not instance.pk:
#         return False
#
#     try:
#         old_file = sender.objects.get(pk=instance.pk).photo
#     except sender.DoesNotExist:
#         return False
#
#     new_file = instance.photo
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
