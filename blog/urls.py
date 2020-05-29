from django.urls import path, include
from .views import (
    #PostDetailView,
    post_detail,
    #PostListView,
    post_list, 
    PostUpdateView, 
    PostDeleteView, 
    PostCreateView,

    CommentUpdateView,
    CommentDeleteView,
)


urlpatterns = [
    path('<int:pk>/<slug:slug>/edit/', 
            PostUpdateView.as_view(), name='post_edit'),
    #path('<int:pk>/<slug:slug>/',
            #PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/<slug:post>/',
            post_detail, name='post_detail'),
    path('<int:pk>/<slug:slug>/delete/',
            PostDeleteView.as_view(), name='post_delete'),
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
   
   #edit and delete url for post comment
   path('<int:pk>/comment_edit/',
        CommentUpdateView.as_view(), name='comment_edit'),
   path('<int:pk>/comment_delete/', 
        CommentDeleteView.as_view(), name='comment_delete')
    
]
