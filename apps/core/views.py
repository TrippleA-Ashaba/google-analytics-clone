import json
from datetime import datetime, timezone
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Min, F, OuterRef, Subquery, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from .helpers.ua_parser import parse_user_agent
from .forms import BusinessForm, PropertyForm, StaffForm
from .models import Business, Property, Staff, StaffRoles, UserActivity

# Create your views here.
User = get_user_model()


@csrf_exempt
def usage(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        timestamp = data.get("timestamp")
        user_agent = data.get("userAgent")
        user_ip = request.META.get("REMOTE_ADDR")
        print("==========================================================")
        print(message)
        print(timestamp)
        print(user_agent)
        print(user_ip)
        print("==========================================================")

        # Process the data, e.g., store it in a database, log it, etc.

        return JsonResponse({"status": "Event tracked successfully"})
    else:
        return JsonResponse({"status": "Invalid request method"})


def vanilla(request):
    return render(request, "vanilla.html")


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "landing_page.html")


@login_required
def dashboard(request):
    user = request.user
    businesses = Business.objects.filter(created_by=user).exists()
    site_users = 0
    new_users = 0

    if not businesses:
        return redirect("business_register")

    try:
        active_website = (
            Property.objects.get(business__created_by=user, is_active=True) or None
        )
    except Property.DoesNotExist:
        active_website = None

    if active_website:
        site_users = (
            UserActivity.objects.filter(website=active_website)
            .values("ip_address")
            .annotate(ip_count=Count("ip_address"))
            .count()
        )
        # Get the current date in the user's timezone (assuming you store timestamps in UTC)
        current_date = datetime.now(timezone.utc).date()

        # Calculate the start and end timestamps for the current day
        start_of_day = datetime.combine(
            current_date, datetime.min.time(), tzinfo=timezone.utc
        )
        end_of_day = datetime.combine(
            current_date, datetime.max.time(), tzinfo=timezone.utc
        )

        earliest_timestamps = (
            UserActivity.objects.filter(
                website=active_website, ip_address=OuterRef("ip_address")
            )
            .values("ip_address")
            .annotate(earliest_timestamp=Min("timestamp"))
            .values("earliest_timestamp")
        )

        # Query for new users for the current day
        new_users = (
            UserActivity.objects.filter(timestamp__range=(start_of_day, end_of_day))
            .annotate(earliest_timestamp=Subquery(earliest_timestamps))
            .filter(timestamp=F("earliest_timestamp"))
        )

        num_countries = (
            UserActivity.objects.filter(website=active_website)
            .values("country")
            .distinct()
            .count()
        )

        # Count the number of distinct cities
        num_cities = (
            UserActivity.objects.filter(website=active_website)
            .values("city")
            .distinct()
            .count()
        )

        country_counts = (
            UserActivity.objects.filter(website=active_website)
            .values("country")
            .annotate(user_count=Count("country"))
            .order_by("-user_count")
        )
        most_common_country = country_counts.first()

        city_counts = (
            UserActivity.objects.filter(website=active_website)
            .values("city")
            .annotate(user_count=Count("city"))
            .order_by("-user_count")
        )
        most_common_city = city_counts.first()

        if most_common_country:
            most_common_country_name = most_common_country["country"]
        else:
            most_common_country_name = "None"

        if most_common_city:
            most_common_city_name = most_common_city["city"]
        else:
            most_common_city_name = "None"

            # Query the most common browser, device, and operating system
        common_browser = (
            UserActivity.objects.filter(website=active_website)
            .values("user_agent")
            .annotate(count=Count("user_agent"))
            .order_by("-count")
            .first()
        )
        if common_browser:
            browser, _, _ = parse_user_agent(common_browser["user_agent"])
            common_browser_name = browser
        else:
            common_browser_name = "Unknown Browser"

        common_device = (
            UserActivity.objects.filter(website=active_website)
            .values("user_agent")
            .annotate(count=Count("user_agent"))
            .order_by("-count")
            .first()
        )
        if common_device:
            _, _, device = parse_user_agent(common_device["user_agent"])
            common_device_name = device
        else:
            common_device_name = "Unknown Device"

        common_os = (
            UserActivity.objects.filter(website=active_website)
            .values("user_agent")
            .annotate(count=Count("user_agent"))
            .order_by("-count")
            .first()
        )
        if common_os:
            _, os, _ = parse_user_agent(common_os["user_agent"])
            common_os_name = os
        else:
            common_os_name = "Unknown OS"

    context = {
        "active_website": active_website,
        "site_users": site_users,
        "new_users": new_users,
        "most_common_country_name": most_common_country_name,
        "most_common_city_name": most_common_city_name,
        "num_cities": num_cities,
        "num_countries": num_countries,
        "common_browser_name": common_browser_name,
        "common_device_name": common_device_name,
        "common_os_name": common_os_name,
    }

    return render(request, "core/dashboard.html", context)


# ==================== Business ================================


@login_required
def business_register(request):
    user = request.user
    if request.method == "POST":
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.created_by = user
            business.save()
            messages.success(
                request,
                f"{business} added successfully",
                extra_tags="bg-success",
            )

    return redirect("show_business")


@login_required
def business_detail(request, id):
    user = request.user
    business = get_object_or_404(Business, id=id, created_by=user)
    properties = business.property.all().order_by("-created_at")
    images = list(range(1, 11))

    form = PropertyForm()
    context = {
        "business": business,
        "form": form,
        "properties": properties,
        "images": images,
    }
    return render(request, "core/business_detail.html", context)


@login_required
def edit_business(request, id):
    user = request.user
    business = get_object_or_404(Business, id=id, created_by=user)
    form = BusinessForm(instance=business)

    if request.method == "POST":
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"{business} edited successfully",
                extra_tags="bg-success",
            )
        return redirect("business_detail", id=business.id)

    context = {"business": business, "form": form}
    return render(request, "partials/business_edit.html", context)


@login_required
def show_business(request):
    user = request.user
    businesses = Business.objects.filter(created_by=user).order_by("-created_at")
    form = BusinessForm()

    context = {"businesses": businesses, "form": form}
    return render(request, "core/business.html", context)


@login_required
def delete_business(request, id):
    user = request.user
    business = get_object_or_404(Business, id=id, created_by=user)

    if request.method == "DELETE":
        business.delete()
        messages.success(
            request,
            f"{business} deleted successfully",
            extra_tags="bg-success",
        )

    return redirect("show_business")


@login_required
def search_business(request):
    user = request.user
    if request.method == "POST":
        businesses = Business.objects.filter(created_by=user).order_by("-created_at")
        search = request.POST.get("search")
        if search:
            businesses = businesses.filter(
                Q(name__icontains=search) | Q(business_sector__icontains=search)
            )
        context = {"businesses": businesses}

        return render(request, "partials/search.html", context)


# ============================= Property ==============================


@login_required
def property_register(request, business_id=id):
    user = request.user
    business = get_object_or_404(Business, id=business_id, created_by=user)
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.business = business
            property.save()
            messages.success(
                request,
                f"{property} added successfully",
                extra_tags="bg-success",
            )
    return redirect("business_detail", id=business_id)


@login_required
def show_properties(request):
    user = request.user
    images = list(range(1, 11))
    properties = Property.objects.filter(business__created_by=user)
    context = {"properties": properties, "images": images}
    return render(request, "core/properties.html", context)


@login_required
def property_detail(request, id):
    user = request.user
    property = get_object_or_404(Property, id=id)
    property_creator = property.business.created_by

    is_editor = False
    try:
        staff = Staff.objects.get(user=user, property=property)
    except Staff.DoesNotExist:
        staff = None
    print(staff)
    if staff and staff.role == "editor":
        is_editor = True

    context = {
        "property": property,
        "property_creator": property_creator,
        "is_editor": is_editor,
    }
    return render(request, "core/property_detail.html", context)


@login_required
def edit_property(request, id):
    property = get_object_or_404(Property, id=id)
    if request.method == "POST":
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"{property} edited successfully", extra_tags="bg-success"
            )
        else:
            messages.error(
                request,
                f"{property} was not edited, check your values. ",
                extra_tags="bg-danger",
            )
        return redirect("business_detail", id=property.business.id)

    context = {"property": property}
    return render(request, "partials/property_edit.html", context)


@login_required
def delete_property(request, id):
    user = request.user
    property = get_object_or_404(Property, id=id, business__created_by=user)
    if request.method == "DELETE":
        property.delete()
        messages.success(
            request, f"{property} deleted successfully", extra_tags="bg-success"
        )

        return HttpResponse(status=200)
    return HttpResponse(status=500)


@login_required
def activate_property(request, id):
    user = request.user
    property = get_object_or_404(Property, id=id)
    if request.method == "POST":
        properties = get_list_or_404(Property, business__created_by=user)
        for item in properties:
            item.is_active = False
            item.save()
        property.is_active = True
        property.save()
        return redirect("business_detail", id=property.business.id)
    return HttpResponse(status=500)


@login_required
def shared_properties(request):
    properties = Property.objects.filter(staff__user=request.user)
    context = {"properties": properties}
    return render(request, "core/shared_properties.html", context)


# =========================== Staff =====================================


@login_required
def staff_add(request, id):
    user = request.user
    property = get_object_or_404(Property, id=id)
    users = User.objects.exclude(id=request.user.id)
    roles = StaffRoles.choices
    if request.method == "POST":
        form = StaffForm(user, request.POST)

        if form.is_valid():
            try:
                staff, created = Staff.objects.get_or_create(
                    user=form.cleaned_data["user"], property=property
                )
                if created:
                    messages.success(
                        request, f"{staff} added successfully", extra_tags="bg-success"
                    )
                    return redirect("business_detail", id=property.business.id)

                else:
                    messages.warning(
                        request,
                        f"{staff} is already staff for this property.",
                        extra_tags="bg-warning",
                    )
                    return redirect("business_detail", id=property.business.id)

            except IntegrityError:
                messages.error(
                    request,
                    "An error occurred. Please try again later.",
                    extra_tags="bg-danger",
                )
            return redirect("business_detail", id=property.business.id)

        else:
            messages.error(
                request,
                "Invalid form data. Please check your inputs.",
                extra_tags="bg-danger",
            )
            return redirect("business_detail", id=property.business.id)

    else:
        form = StaffForm(user)

    context = {"users": users, "property": property, "roles": roles, "form": form}
    return render(request, "partials/staff_add.html", context)


@login_required
def edit_staff(request, id):
    user = request.user
    staff = get_object_or_404(Staff, id=id, property__business__created_by=user)
    if request.method == "POST":
        form = StaffForm(user, request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Staff edited successfully", extra_tags="bg-success"
            )
            return redirect("property_detail", id=staff.property.id)
    form = StaffForm(user, instance=staff)
    context = {"form": form}
    return render(request, "core/staff_register.html", context)


@login_required
def remove_staff(request, id):
    user = request.user
    staff = get_object_or_404(Staff, id=id, property__business__created_by=user)
    staff.delete()
    messages.success(request, "Staff Removed successfully", extra_tags="bg-success")
    return redirect("property_detail", id=staff.property.id)
