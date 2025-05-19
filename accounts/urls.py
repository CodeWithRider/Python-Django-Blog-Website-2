from django.urls import path
from .views import signup, signin, logout, UserProfileView, UserProfileEditView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout, name='logout'),
    path('profile/<int:id>/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/<int:id>/', UserProfileEditView.as_view(), name='profileedit'),
]
