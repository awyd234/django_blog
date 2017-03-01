# -*- coding: utf-8 -*-

from django import forms
from .models import Article, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Category


class BlogCommentForm(forms.ModelForm):
    class Meta:
        '''
        指定一些Meta选项以改变form被渲染后的样式
        '''
        model = Comment
        fields = ['body']

        widgets = {
            # 'user': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': '请输入用户id(临时)',
            #     'aria-describedby': 'sizing-addon1',
            # }),
            'body': forms.Textarea(attrs={
                'placeholder': '请输入评论',
            })
        }


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'category', 'abstract', 'body', 'status', 'topped')

    def __init__(self, *args, **kwargs):
        super(PostAddForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['title'].label = '标题'
        self.fields['title'].label_class = 'col-lg-2'
        self.fields['body'].label = '正文'
        self.fields['body'].help_text = '支持Markdown语法标记'
        self.fields['category'].queryset = Category.objects.filter(user_id=kwargs['initial'].get('user').id)
        if self.initial.get('category') == 0:
            self.fields['category'].widget = forms.HiddenInput()


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'category', 'abstract', 'body')

    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['category'].queryset = Category.objects.filter(user_id=kwargs['instance'].user_id)
        self.fields['title'].label = '标题'
        self.fields['title'].label_class = 'col-lg-2'
        self.fields['body'].label = '正文'
        self.fields['body'].help_text = '支持Markdown语法标记'
