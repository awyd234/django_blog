# -*- coding: utf-8 -*-

from django import forms
from models import Article, Comment


class BlogCommentForm(forms.ModelForm):
    class Meta:
        '''
        指定一些Meta选项以改变form被渲染后的样式
        '''
        model = Comment
        fields = ['user', 'body']

        widgets = {
            'user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入用户id(临时)',
                'aria-describedby': 'sizing-addon1',
            }),
            'body': forms.Textarea(attrs={
                'placeholder': '请输入评论',
            })
        }
