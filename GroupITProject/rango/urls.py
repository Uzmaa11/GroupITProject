from django.urls import path
from rango import views


app_name = 'rango'
urlpatterns = [
path('', views.index, name='index'),
# path('about/', views.about, name='about'),
path('login/', views.login, name='login'),
path('register/', views.register, name='register'),
path('upload/', views.upload, name='upload'),
path('blogs/', views.blog_list, name='blogs'),
path('UserProfile/', views.UserProfile, name='UserProfile'),
path('admin/',views.admin, name='admin'),


]

from django.urls import path
from .views import admin_login, dashboard, new_post

urlpatterns = [
    path('login/', admin_login, name='admin_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('new_post/', new_post, name='new_post'),
    path('upload/', views.BlogCreateView.as_view(), name='upload'),
    path('blogs/', views.blog_list, name='blogs'),
]
