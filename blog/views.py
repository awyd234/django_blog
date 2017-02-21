# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models.aggregates import Count
from blog.models import Article, Category
import markdown2


class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        articles_list = Article.objects.filter(status='p').order_by('created_time')
        for article in articles_list:
            article.body = markdown2.markdown(article.body, )
        return articles_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name').annotate(num_articles=Count('article'))
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )

        article_id = obj.id
        article = Article.objects.get(id=article_id)
        article.views = article.views + 1
        article.save()

        obj.views = article.views

        return obj


class CategoryView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"
    pk_url_kwarg = "cate_id"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name').annotate(num_articles=Count('article'))
        kwargs['active_category'] = Category.objects.all().filter(id=self.kwargs['cate_id'])[0]
        return super(CategoryView, self).get_context_data(**kwargs)
