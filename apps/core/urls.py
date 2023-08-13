from django.urls import path

from .views import (
    business_register,
    home,
    landing_page,
    show_businesses,
    staff_register,
    show_staff,
)

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("dashboard/", home, name="home"),
    path("add-business/", business_register, name="business_register"),
    path("businesses/", show_businesses, name="show_businesses"),
    path("staff_register/", staff_register, name="staff_register"),
    path("staff/", show_staff, name="show_staff"),
]
