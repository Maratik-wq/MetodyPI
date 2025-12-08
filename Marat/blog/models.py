from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Club(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название клуба"))
    country = models.CharField(max_length=100, verbose_name=_("Страна"))
    founded = models.IntegerField(verbose_name=_("Год основания"))
    stadium = models.CharField(max_length=100, verbose_name=_("Стадион"))
    logo = models.ImageField(
        upload_to='logos/',
        verbose_name=_("Логотип"),
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Заголовок"))
    content = models.TextField(verbose_name=_("Содержание"))
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата публикации"))
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts', verbose_name=_("Клуб"))
    author = models.CharField(max_length=100, verbose_name=_("Автор"))

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Автор"))
    subject = models.CharField(max_length=150, verbose_name=_("Тема"))
    text = models.TextField(max_length=1000, verbose_name=_("Текст комментария"))
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name=_("Опубликован"))

    def __str__(self):
        return f"{self.subject} — {self.author.username}"

    class Meta:
        ordering = ['-created_at']
