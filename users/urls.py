from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, LoginView, LogoutView, ProfileView, my_profile_redirect, ProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/', my_profile_redirect, name='my_profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),
]
