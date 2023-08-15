from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from apps.accounts.models import CustomUser

from .forms import BusinessForm, StaffForm, PropertyForm
from .models import Business, Property, Staff
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "landing_page.html")


@login_required
def home(request):
    businesses = Business.objects.filter(created_by=request.user).exists()
    if not businesses:
        return redirect("business_register")
    return render(request, "core/index.html")


# ==================== Business ================================


@login_required
def business_register(request):
    user = request.user
    form = BusinessForm()

    if request.method == "POST":
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.created_by = user
            business.save()
            return redirect("property_register")
    return render(request, "core/business_register.html", {"form": form})


@login_required
def edit_business(request, id):
    user = request.user
    business = get_object_or_404(Business, id=id, created_by=user)
    form = BusinessForm(instance=business)
    if request.method == "POST":
        form = BusinessForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return redirect("show_businesses")
    return render(request, "core/business_edit.html", {"form": form})


@login_required
def show_businesses(request):
    user = request.user
    businesses = Business.objects.filter(created_by=user)
    context = {"businesses": businesses}
    return render(request, "core/businesses.html", context)


@login_required
def delete_business(request, id):
    user = request.user
    business = get_object_or_404(id=id, created_by=user)
    business.delete()
    return redirect("show_businesses")


# ============================= Property ==============================


@login_required
def property_register(request):
    user = request.user
    form = PropertyForm(user)
    if request.method == "POST":
        form = PropertyForm(user, request.POST)
        if form.is_valid():
            form.save()
        return redirect("show_properties")
    return render(request, "core/property_register.html", {"form": form})


@login_required
def show_properties(request):
    user = request.user
    images = list(range(1, 11))
    properties = Property.objects.filter(business__created_by=user)
    context = {"properties": properties, "images": images}
    return render(request, "core/properties.html", context)


@login_required
def property_detail(request, id):
    property = get_object_or_404(Property, id=id)
    context = {"property": property}
    return render(request, "core/property_detail.html", context)


@login_required
def edit_property(request, id):
    user = request.user
    property = get_object_or_404(Property, id=id, business__created_by=user)
    form = PropertyForm(user=user, instance=property)
    if request.method == "POST":
        form = PropertyForm(user, request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect("show_properties")
    return render(request, "core/property_edit.html", {"form": form})


@login_required
def delete_property(request, id):
    user = request.user
    property = get_object_or_404(Property, id=id, business__created_by=user)
    property.delete()
    return redirect("show_properties")


# =========================== Staff =====================================


@login_required
def staff_register(request):
    user = request.user
    if request.method == "POST":
        form = StaffForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_properties")

    form = StaffForm(user)
    context = {"form": form}
    return render(request, "core/staff_register.html", context)


@login_required
def edit_staff(request, id):
    user = request.user
    staff = get_object_or_404(Staff, id=id, property__business__created_by=user)
    if request.method == "POST":
        form = StaffForm(user, request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect("property_detail", id=staff.property.id)
    form = StaffForm(user, instance=staff)
    context = {"form": form}
    return render(request, "core/staff_register.html", context)


@login_required
def remove_staff(request, id):
    user = request.user
    staff = get_object_or_404(Staff, id=id, property__business__created_by=user)
    staff.delete()
    messages.success(request, "Staff member deleted successfully.")
    return redirect("property_detail", id=staff.property.id)
