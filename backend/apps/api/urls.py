from django.urls import path, include
from .views import (
    UserRegister,
    ListSecureDropUsers,
    LoginSecureDropUsers
)

urlpatterns = [
    path('register', UserRegister.as_view()),
    path('lookup', ListSecureDropUsers.as_view()),
    path('login', LoginSecureDropUsers.as_view()),
]