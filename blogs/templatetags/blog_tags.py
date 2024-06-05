from django import template
from blogs.models import Post
from django.shortcuts import render
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register=template.Library()

@register.simple_tag(name='my_blogs')
def total_posts():
    return Post.objects.only('published').count()

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comment')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))