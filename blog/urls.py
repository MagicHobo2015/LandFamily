from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('contact/', views.contact, name='blog-contact'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='Post-Detail'),
    path('post/<int:pk>/new_comment/', views.CommentCreateView.as_view(), name='post-comment'),
    path('post/new_post/', views.PostCreateView.as_view(), name='post-create'),
    path('post/list/', views.PostListView.as_view(), name='post-list'),
    path('<int:year>/<int:month>/', views.PostMonthArchiveView.as_view(month_format='%m'), name='post-month-archive'),
    path('post/<int:pk>/confirm_delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/update_comment', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/confirm_delete', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/update_post/', views.PostUpdateView.as_view(), name='post-update'),
    path('latest_posts/', views.PostArchiveIndexView.as_view(), name='latest_posts'),

]
