# Generated by Django 3.0.5 on 2020-09-21 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20200904_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='default/profile-picture.png', upload_to='user/%Y/%m/%d/', verbose_name='фото профілю'),
        ),
    ]