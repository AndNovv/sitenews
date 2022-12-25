from django.db import models

class Newsblock(models.Model):
    source_favicon = models.CharField('Логотип издания', max_length=200, default='0', blank=True)
    source_url = models.CharField('Ссылка', max_length=200, default='/article', blank=True)
    title = models.CharField('Заголовок статьи', max_length=200, default='Заголовок статьи')
    source_id = models.IntegerField('Идентификатор источника', default=0, blank=True, null=True)
    views_count = models.IntegerField('Кол-во просмотров', default=0, blank=True, null=True)
    new = models.BooleanField('Отправлять уведомление', default=True)
    text = models.TextField('Текст статьи', max_length=5000, default='Текст Статьи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Source(models.Model):
    source_id = models.IntegerField('Идентификатор источника', default=0)
    source_favicon = models.CharField('Логотип издания', max_length=200, default='0')
    source_name = models.CharField('Название источника', max_length=20, default='0')
    source_name_form = models.CharField('Название источника для формы', max_length=20, default='0')

    def __str__(self):
        return self.source_name

    class Meta:
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'

class User(models.Model):
    user_name = models.CharField('Имя и Фамилия', max_length=40, default='0')
    user_login = models.CharField('Логин', max_length=20, default='0')
    user_password = models.CharField('Пароль', max_length=30, default='0')
    viewed_news = models.ManyToManyField(Newsblock)
    followed_sources = models.ManyToManyField(Source)
    telegram_notification = models.BooleanField('Отправлять уведомления?', default=False)
    telegram_userid = models.CharField('Логин', max_length=20, default='0')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
