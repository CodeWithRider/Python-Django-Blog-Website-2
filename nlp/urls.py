from django.urls import path
from .views import qna_view

urlpatterns = [
    path('qna/', qna_view, name='qna'),
]
