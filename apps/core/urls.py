from django.urls import path

from .views import (
    business_register,
    home,
    landing_page,
    show_businesses,
    staff_register,
    property_register,
    show_properties,
    property_detail,
)

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("dashboard/", home, name="home"),
    path("add-business/", business_register, name="business_register"),
    path("businesses/", show_businesses, name="show_businesses"),
    path("staff_register/", staff_register, name="staff_register"),
    path("property_register/", property_register, name="property_register"),
    path("properties/", show_properties, name="show_properties"),
    path("property_detail/<int:id>/", property_detail, name="property_detail"),
]
