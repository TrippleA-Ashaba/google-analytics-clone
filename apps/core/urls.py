from django.urls import path

from .views import home, landing_page

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("dashboard/", home, name="home"),
]
