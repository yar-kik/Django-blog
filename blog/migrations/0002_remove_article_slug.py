# Generated by Django 3.2.5 on 2021-07-03 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='slug',
        ),
    ]