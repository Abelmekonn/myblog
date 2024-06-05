from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','published','status')
    list_filter=('status','published','author','created')
    search_fields=('author','body')
    prepopulated_fields={'slug':('title',)}
    raw_id_fields=('author')
    date_hierarchy='published'
    ordering=('status','published') 

class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','post','created','active')
    list_filter=('active','created','updated')
    search_fields=('name','email','body')