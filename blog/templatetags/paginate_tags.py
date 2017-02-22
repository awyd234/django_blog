# -*- coding: utf-8 -*-
from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()


@register.simple_tag(takes_context=True)
def paginate(context, object_list, page_count):
    '''
    对template分页
    :param context: 上下文变量
    :param object_list: 需要分页的内容
    :param page_count: 每页的数量
    :return:
    '''
    left = 2
    right = 2

    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page')

    try:
        object_list = paginator.page(page)
        context['current_page'] = int(page)
        pages = get_left(context['current_page'], left, paginator.num_pages)\
                + get_right(context['current_page'], right, paginator.num_pages)
    except PageNotAnInteger:
        object_list = paginator.page(1)
        context['current_page'] = 1
        pages = get_right(context['current_page'], right, paginator.num_pages)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = get_left(context['current_page'], left, paginator.num_pages)

    context['article_list'] = object_list
    context['pages'] = pages
    context['last_page'] = paginator.num_pages
    context['first_page'] = 1

    try:
        context['pages_first'] = pages[0]
        context['pages_last'] = pages[-1] + 1
    except IndexError:
        context['pages_first'] = 1
        context['pages_last'] = 2
    return ''
    # 去掉试试


def get_left(current_page, left, num_pages):
    '''
    获取左侧的页码
    :param current_page: 当前页码
    :param left: 左侧包含几页
    :param num_pages: 总页数
    :return:
    '''
    if current_page == 1:
        return []
    elif current_page == num_pages:
        l = [i - 1 for i in range(current_page, current_page - left, -1) if i - 1 > 1]
    else:
        l = [i for i in range(current_page, current_page - left, -1) if i > 1]
    l.sort()
    return l


def get_right(current_page, right, num_pages):
    '''
    获取右侧的页码
    :param current_page: 当前页码
    :param right: 右侧包含几页
    :param num_pages: 总页数
    :return:
    '''
    if current_page == num_pages:
        return []
    l = [i + 1 for i in range(current_page, current_page + right - 1) if i < num_pages - 1]
    return l
