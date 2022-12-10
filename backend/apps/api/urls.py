from django.urls import path, include
from .views import (
    UserRegister,
    ListSecureDropUsers
)

urlpatterns = [
    path('register', UserRegister.as_view()),
    path('lookup', ListSecureDropUsers.as_view()),
]