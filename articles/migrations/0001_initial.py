# Generated by Django 3.2.4 on 2021-06-05 14:15

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('archives', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, choices=[('film', 'Фільми'), ('game', 'Ігри'), ('anime', 'Аніме')], default='film', max_length=16, verbose_name='категорія')),
                ('title', models.CharField(max_length=100, verbose_name='назва статті')),
                ('text', models.TextField(max_length=20000, verbose_name='текст')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='дата створення')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='дата редагування')),
                ('slug', models.SlugField(max_length=100)),
                ('status', models.CharField(blank=True, choices=[('draft', 'Чернетка'), ('moderation', 'На модерації'), ('publish', 'Опублікований')], default='draft', max_length=16, verbose_name='статус')),
                ('large_picture', imagekit.models.fields.ProcessedImageField(blank=True, default='default/large-article-picture.jpg', upload_to='articles/large/', verbose_name='картинка для ПК')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('related_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='archives.infobase')),
                ('users_bookmark', models.ManyToManyField(blank=True, related_name='articles_bookmarked', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True, related_name='articles_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_created',),
                'permissions': [('can_moderate_article', 'Може одобрювати статті'), ('can_draft_article', 'Може створювати чернетку статті')],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=2000, verbose_name='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('path', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=list, size=None)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='articles.article')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True, related_name='comments_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]