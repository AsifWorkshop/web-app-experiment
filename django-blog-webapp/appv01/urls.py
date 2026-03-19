from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.feed_func,name='feed'),
    path('feed/',views.feed_func,name='feed'),
    path('create-post/', views.create_post_view, name='create_post'),
    path('login/',views.login_view,name='login'),
    path('registration/',views.registration_view,name='registration'),
    path('profile/',views.profile_view,name='profile'),
    # path('comment/', views.comment_view, name='comment'),
    # path('comment/<int:post_id>/', views.comment_view, name='comment'),
    path('logout/',views.logout_view,name='logout'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comments/', views.comment_page, name='comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('get-comment-count/<int:post_id>/', views.get_comment_count, name='get_comment_count'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search-posts/', views.search_posts, name='search_posts'),
]