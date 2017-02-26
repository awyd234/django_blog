# -*- coding: utf-8 -*-

from django.db import models
from config import settings
from django.core.urlresolvers import reverse


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now_add=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    abstract = models.CharField('摘要', max_length=54, blank=True,
                                null=True, help_text="可选，如若为空则摘取文章前54个字符")
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户id")
    category = models.ForeignKey('Category', verbose_name='分类', null=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_modified_time']

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'article_id': self.pk})


class Category(models.Model):
    name = models.CharField('类名', max_length=20)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户id")

    def __str__(self):
        return self.name


class Comment(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    edit_time = models.DateTimeField('修改时间', auto_now_add=True)
    update_time = models.DateTimeField('最近更新时间', auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户id")
    article = models.ForeignKey('Article', verbose_name='文章所属id')
    body = models.TextField('评论内容')

    def __str__(self):
        return self.name
