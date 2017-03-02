"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
#from userena import views as userena_views
from . import views

urlpatterns = [
    url(r'^(?P<username>[0-9a-zA-Z]+)$', views.IndexView.as_view(), name='home'),
    url(r'^(?P<username>[0-9a-zA-Z]+)/article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),# to learn
    url(r'^(?P<username>[0-9a-zA-Z]+)/category/(?P<cate_id>\d+)$', views.CategoryView.as_view(), name='category'),
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.PostEditView.as_view(), name='edit'),
    url(r'^post/(?P<cate_id>[0-9]+)/add/$', views.PostAddView.as_view(), name='add'),
    url(r'^article-like', views.ajax_article_like, name='ajax-article-like'),
    url(r'^category-add', views.ajax_category_add, name='ajax_category_add'),
]
