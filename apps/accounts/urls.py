from django.urls import path

from .views import SignUpView, user_login, user_logout

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
]
