from django.urls import path
from rango import views
from .views import admin_login, dashboard, new_post
from .views import delete_blog
from . import views

app_name = 'rango'
urlpatterns = [
path('', views.index, name='index'),
# path('about/', views.about, name='about'),
path('login/', views.user_login, name='user_login'),
path('register/', views.register, name='register'),
path('upload/', views.BlogCreateView.as_view(), name='upload'),
path('blogs/', views.blog_list, name='blogs'),
path('UserProfile/', views.UserProfile, name='UserProfile'),
path('admin/',views.admin, name='admin'),
]

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('new_post/', new_post, name='new_post'),
    path('blogs/', views.blog_list, name='blogs'),
]
urlpatterns = [
    path('blog/<int:blog_id>/delete/', delete_blog, name='delete_blog'),
]

urlpatterns = [
    path('blog/search/', views.blog_search, name='blog_search'),
]
