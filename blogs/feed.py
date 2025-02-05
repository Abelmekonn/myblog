from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils.safestring import SafeText
from .models import Post


class LatestPostFeed(Feed):
    title = 'My Blog'
    link=reverse_lazy('blogs:post_list')
    description = 'New posts of my blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
    
