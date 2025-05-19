from django.urls import path
from .views import (
    PostCreateView, PostDetailView, PostUpdateView, PostDeleteView,
    savecomment, deletecomment, increaselikes
)

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='editpost'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='deletepost'),
    path('post/<int:id>/comment/', savecomment, name='savecomment'),
    path('comment/delete/<int:id>/', deletecomment, name='deletecomment'),
    path('like/<int:id>/', increaselikes, name='increaselikes'),
]
