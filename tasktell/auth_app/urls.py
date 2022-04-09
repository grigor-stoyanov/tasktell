from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from tasktell.auth_app.views.auth import UserLoginView, UserProfileRegisterView, ResetPasswordView
from tasktell.auth_app.views.profile import ProfileDetailsView, EditProfileView, DeleteProfileView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserProfileRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile'),
    path('edit/profile/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
    path('delete/profile/<int:pk>/', DeleteProfileView.as_view(), name='delete profile'),
    path('password-reset/', ResetPasswordView.as_view(), name='reset password'),
    path('logout/', LogoutView.as_view(template_name="home.html", next_page=reverse_lazy('home')), name='logout'),
]
