from django.urls import path
from .views import AccountView, SigninView

urlpatterns = [
    path('/signup', AccountView.as_view()),
    path('/signin', SigninView.as_view()),
]