from django.urls import path

from .apiviews import UserActivityApiView
from .views import (
    activate_property,
    business_detail,
    business_register,
    dashboard,
    delete_business,
    delete_property,
    edit_business,
    edit_property,
    landing_page,
    property_detail,
    property_register,
    property_select,
    property_select_activate,
    search_business,
    show_business,
    show_properties,
    staff_add,
)

urlpatterns = [
    path("", landing_page, name="landing_page"),
    # ============== Dashboard =======================
    path("dashboard/", dashboard, name="dashboard"),
    path("property_select/", property_select, name="property_select"),
    path(
        "property_select_activate/",
        property_select_activate,
        name="property_select_activate",
    ),
    # ========== business =============
    path("business_register/", business_register, name="business_register"),
    path("businesses/", show_business, name="show_business"),
    path("business/<int:id>/detail", business_detail, name="business_detail"),
    path("business/<int:id>/delete/", delete_business, name="delete_business"),
    path("business/<int:id>/edit/", edit_business, name="edit_business"),
    path("search_business/", search_business, name="search_business"),
    # ========== staff =========
    path("property/<int:id>/staff_add/", staff_add, name="staff_add"),
    # path("staff/<int:id>/remove", remove_staff, name="remove_staff"),
    # path("staff/<int:id>/edit/", edit_staff, name="edit_staff"),
    # ========== property ===========
    path(
        "business/<int:business_id>/add_property/",
        property_register,
        name="property_register",
    ),
    path("properties/", show_properties, name="show_properties"),
    path("property/<int:id>/detail/", property_detail, name="property_detail"),
    path("property/<int:id>/delete/", delete_property, name="delete_property"),
    path("property/<int:id>/edit/", edit_property, name="edit_property"),
    path(
        "property/<int:id>/activate_property/",
        activate_property,
        name="activate_property",
    ),
    # path("property/shared/", shared_properties, name="shared_properties"),
    # ================================================
    path(
        "api/user_activity/<str:web_token>/",
        UserActivityApiView.as_view(),
        name="user_activity",
    ),
]
