from django.urls import path

from .views import home, landing_page, business_register, show_businesses

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("dashboard/", home, name="home"),
    path("add-business/", business_register, name="business_register"),
    path("businesses/", show_businesses, name="show_businesses"),
]
