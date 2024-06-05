from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

from .feed import LatestPostFeed
app_name='blogs'
urlpatterns = [
    path('tag/<slug:tag_slug>/',views.post_list,name='post_list'),
    path('',views.post_list,name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/',views.post_share,name="post_share"),
    path('feed/', LatestPostFeed(), name='feed'),
    path('post-create/', views.Post_Create.as_view(), name='post-create'),
    path('update-task/<int:pk>/',views.Post_Update.as_view(),name='update-task'),
    path('login/',views.login_view,name='login'),
    # path('register/',views.RegisterPage.as_view(),name='register'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
]
