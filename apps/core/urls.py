from django.urls import path

from .views import (
    business_register,
    delete_business,
    delete_property,
    edit_business,
    edit_property,
    edit_staff,
    dashboard,
    landing_page,
    property_detail,
    property_register,
    remove_staff,
    shared_properties,
    show_business,
    show_properties,
    staff_register,
    vanilla,
)

urlpatterns = [
    path("vanilla/", vanilla, name="vanilla"),
    path("", landing_page, name="landing_page"),
    path("dashboard/", dashboard, name="dashboard"),
    # ========== business =============
    path("business_register/", business_register, name="business_register"),
    path("businesses/", show_business, name="show_business"),
    # path("business/<int:id>/delete/", delete_business, name="delete_business"),
    # path("business/<int:id>/edit/", edit_business, name="edit_business"),
    # ========== staff =========
    # path("staff_register/", staff_register, name="staff_register"),
    # path("staff/<int:id>/remove", remove_staff, name="remove_staff"),
    # path("staff/<int:id>/edit/", edit_staff, name="edit_staff"),
    # ========== property ===========
    path("property_register/", property_register, name="property_register"),
    path("properties/", show_properties, name="show_properties"),
    path("property/<int:id>/detail/", property_detail, name="property_detail"),
    # path("property/<int:id>/delete/", delete_property, name="delete_property"),
    # path("property/<int:id>/edit/", edit_property, name="edit_property"),
    # path("property/shared/", shared_properties, name="shared_properties"),
]
