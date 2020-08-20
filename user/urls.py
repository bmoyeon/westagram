from django.urls import path
from .views import (
    AccountView,
    SigninView
)

urlpatterns = [
    path('/sign-up', AccountView.as_view()),
    path('/sign-in', SigninView.as_view()),
]
