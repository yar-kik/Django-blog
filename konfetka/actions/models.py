from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    """Збереження інормації про активність користувача
    Атрибути:
    user - користувач, який виконав дію. Пов'язаний зі стандартною моделлю User
    verb - інформація про те, яка дія була виконана
    created - дата і час створення об'єкту
    target_ct - зовнішній ключ на модель ContentType
    target_id - для збереження ідентифікатора на зв'язанний об'єкт
    target - поле для звернення до з'язаного об'єкту на основі його типу та ідентифікатора"""

    user = models.ForeignKey('auth.User', related_name='actions',
                             db_index=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True,
                                  related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ('-created',)
