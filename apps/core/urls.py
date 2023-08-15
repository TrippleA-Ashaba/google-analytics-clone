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
    delete_property,
    delete_business,
    edit_business,
    edit_property,
    remove_staff,
    edit_staff,
    shared_properties,
)

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("dashboard/", home, name="home"),
    # ========== business =============
    path("add-business/", business_register, name="business_register"),
    path("businesses/", show_businesses, name="show_businesses"),
    path("business/<int:id>/delete/", delete_business, name="delete_business"),
    path("business/<int:id>/edit/", edit_business, name="edit_business"),
    # ========== staff =========
    path("staff_register/", staff_register, name="staff_register"),
    path("staff/<int:id>/remove", remove_staff, name="remove_staff"),
    path("staff/<int:id>/edit/", edit_staff, name="edit_staff"),
    # ========== property ===========
    path("property_register/", property_register, name="property_register"),
    path("properties/", show_properties, name="show_properties"),
    path("property/<int:id>/detail/", property_detail, name="property_detail"),
    path("property/<int:id>/delete/", delete_property, name="delete_property"),
    path("property/<int:id>/edit/", edit_property, name="edit_property"),
    path("property/shared/", shared_properties, name="shared_properties"),
]
