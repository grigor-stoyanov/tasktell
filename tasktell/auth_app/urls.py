from django.urls import path

from tasktell.auth_app.views.auth import UserLoginView, UserProfileRegisterView
from tasktell.auth_app.views.profile import ProfileDetailsView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserProfileRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='register'),
]
