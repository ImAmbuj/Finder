from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="account"),
    path('logout', views.logout, name="logout"),
    path('Home', views.home, name="home"),
    path('Profile/<str:username>', views.profile, name="profile"),
    path('follow/<str:username>', views.handle_follows, name="follow"),
    path('like/<int:id>', views.handle_likes, name="likes"),
    path('save/<int:id>', views.handle_saves, name="saves"),
    path('delete/<int:id>', views.delete_post, name="delete_post"),
    path('Users', views.users, name="users"),
    path('Saved', views.saved_posts, name="saved_posts")
]