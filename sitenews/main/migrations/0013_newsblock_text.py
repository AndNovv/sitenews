# Generated by Django 3.2.7 on 2022-12-04 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20221129_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsblock',
            name='text',
            field=models.CharField(default='0', max_length=5000, verbose_name='Текст статьи'),
        ),
    ]
