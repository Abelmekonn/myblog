from django.shortcuts import render, get_object_or_404,redirect
from .models import Post,Comment
from django.http import request
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from .form import EmailPostForm,CommentForm,LoginForm,RegisterForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.urls import reverse_lazy


def post_list(request,tag_slug=None):
    posts = Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Post,slug=tag_slug)
        posts=posts.filter(tag__in=[tag])
    paginator=Paginator(posts,3)
    
    paginator=Paginator(posts,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request, 'post/list.html', {'posts': posts,'page':page})

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                            status='published',
                            published__year=year,
                            published__month=month,
                            published__day=day,
                            slug=slug)
    comments=Comment.objects.filter(active=True)
    # if comments.post==Post.title:
    #     comment=comments
    new_comment=None
    if request.method=='POST':
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    
    post_tags_ids=Post.tags.values_list('id',flat=True)
    similar_posts=Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-published')[:4]
    
    return render(request, 'post/detail.html', {'post': post,
                                                'comment_form':comment_form,
                                                'new_comment':new_comment,
                                                'comments':comments,
                                                'similar_posts':similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comment']}"
            send_mail(subject, message, 'Abelmekonn8@gamil.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'post/share.html', {'form': form, 'sent': sent})

class Post_Update(UpdateView):
    model=Post
    fields=['title','body','published'] 
    template_name='pos/post_form.html'

class Post_Create(CreateView):
    model = Post
    fields=['title','body','published','status']
    template_name='pos/post_form.html'
    success_url=reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(Post_Create,self).form_valid(form)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(post_list)  
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'post/login.html', {'form': form})

def register_view(request,self):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            if user==None:
                login(self.request,user)
                return redirect(login_view)
            else:
                form.add_error(None,'Invalid input')
    
    return render(request,'post/register.html',{'form':form})