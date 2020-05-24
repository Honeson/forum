from django.urls import path, include
from .views import (
    PostDetailView,
    PostListView, 
    PostUpdateView, 
    PostDeleteView, 
    PostCreateView
)


urlpatterns = [
    path('<int:pk>/<slug:slug>/edit/', 
            PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/<slug:slug>/',
            PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/<slug:slug>/delete/',
            PostDeleteView.as_view(), name='post_delete'),
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('', PostListView.as_view(), name='post_list'),
]
