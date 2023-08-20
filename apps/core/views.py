from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BusinessForm, PropertyForm, StaffForm
from .models import Business, Property, Staff

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
            messages.success(
                request,
                f"{business} edited successfully",
                extra_tags="bg-success",
            )
            return redirect("property_register")
    return render(request, "core/businesses.html", {"form": form})


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
            return redirect("show_businesses")
    return render(request, "partials/form.html", {"form": form})


@login_required
def show_businesses(request):
    user = request.user
    businesses = Business.objects.filter(created_by=user)
    form = BusinessForm()

    context = {"businesses": businesses, "form": form}
    return render(request, "core/businesses.html", context)


@login_required
def delete_business(request, id):
    user = request.user
    business = get_object_or_404(Business, id=id, created_by=user)
    business.delete()
    businesses = Business.objects.filter(created_by=user)
    form = BusinessForm()

    context = {"businesses": businesses, "form": form}
    return render(request, "core/businesses.html", context)


# ============================= Property ==============================


@login_required
def property_register(request):
    user = request.user
    form = PropertyForm(user)
    if request.method == "POST":
        form = PropertyForm(user, request.POST)
        if form.is_valid():
            property = form.cleaned_data["name"]
            form.save()
            messages.success(
                request,
                f"{property} added successfully",
                extra_tags="bg-success",
            )
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
    user = request.user
    property = get_object_or_404(Property, id=id, business__created_by=user)
    form = PropertyForm(user=user, instance=property)

    if request.method == "POST":
        form = PropertyForm(user, request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Property edited successfully", extra_tags="bg-success"
            )
            return redirect("show_properties")

    context = {"form": form}
    return render(request, "core/property_edit.html", context)


@login_required
def delete_property(request, id):
    user = request.user
    property = get_object_or_404(Property, id=id, business__created_by=user)
    property.delete()
    messages.success(request, "Property deleted successfully", extra_tags="bg-success")
    return redirect("show_properties")


@login_required
def shared_properties(request):
    properties = Property.objects.filter(staff__user=request.user)
    context = {"properties": properties}
    return render(request, "core/shared_properties.html", context)


# =========================== Staff =====================================


@login_required
def staff_register(request):
    user = request.user
    if request.method == "POST":
        form = StaffForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Staff added successfully", extra_tags="bg-success"
            )
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
