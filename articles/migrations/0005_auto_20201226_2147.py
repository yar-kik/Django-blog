# Generated by Django 3.0.5 on 2020-12-26 21:47

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20201226_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='middle_picture',
        ),
        migrations.AddField(
            model_name='article',
            name='medium_picture',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='default/medium-article-picture.jpg', upload_to='articles/medium/', verbose_name='картинка для планшетів'),
        ),
    ]