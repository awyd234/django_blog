# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.db.models.aggregates import Count, Aggregate
from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from blog.models import Article, Category, Comment, User

from .models import Comment
from .forms import BlogCommentForm
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
        # todo annotate的用法，count的意思
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
        article.views += 1
        article.save()

        obj.views = article.views

        return obj

    def get_context_data(self, **kwargs):
        comment_list = self.object.comment_set.all()
        no_count = 1
        for comment in comment_list:
            comment.body = markdown2.markdown(comment.body)
            comment.no = no_count
            no_count += 1
        kwargs['comment_list'] = comment_list
        kwargs['form'] = BlogCommentForm()
        return super(ArticleDetailView, self).get_context_data(**kwargs)


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


class CommentPostView(FormView):
    form_class = BlogCommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        comment = form.save(commit=False)
        comment.article = target_article
        comment.save()

        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
        return render(self.request, 'blog/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.comments_set.all()
        })
