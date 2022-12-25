# Generated by Django 3.2.7 on 2021-10-06 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20210919_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsblock',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во просмотров'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='0', max_length=40, verbose_name='Имя и Фамилия')),
                ('user_login', models.CharField(default='0', max_length=20, verbose_name='Логин')),
                ('user_password', models.CharField(default='0', max_length=30, verbose_name='Пароль')),
                ('viewed_news', models.ManyToManyField(to='main.Newsblock')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
