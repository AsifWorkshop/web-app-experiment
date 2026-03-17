from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.welcome),
    path('feed/',views.feed_func,name='feed'),
    path('create-post/', views.create_post_view, name='create_post'),
    path('login/',views.login_view,name='login'),
    path('registration/',views.registration_view,name='registration')
]