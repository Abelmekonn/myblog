from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishManage(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default='draft')
    
    tags=TaggableManager()
    imagefield=models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url=self.imagefield.url
        except:
            url=''
        return url
    objects=models.Manager()
    published_posts = PublishManage()
    
    class Meta:
        ordering = ('-published',)
    
    
    def get_absolute_url(self):
        return reverse('blogs:post_detail', args=[self.published.year,
                                                self.published.month,
                                                self.published.day,
                                                self.slug])


    def __str__(self):
        return self.title

class Comment(models.Model):
    post=models.ForeignKey(Post,
                        on_delete=models.CASCADE,
                        related_name='comment')
    name=models.CharField(max_length=80)
    email=models.EmailField()
    body=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    
    class Meta():
        ordering=('created',)
    def __str__(self) -> str:
        return f'Comment by {self.name}'

