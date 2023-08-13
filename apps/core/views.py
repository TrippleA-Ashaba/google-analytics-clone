from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.models import CustomUser

from .forms import BusinessForm, StaffForm
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
            return redirect("show_businesses")
    return render(request, "core/business_register.html", {"form": form})


@login_required
def show_businesses(request):
    businesses = Business.objects.all()
    context = {"businesses": businesses}
    return render(request, "core/businesses.html", context)


def staff_register(request):
    form = StaffForm()
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("show_staff")

    context = {"form": form}
    return render(request, "core/staff_register.html", context)


def show_staff(request):
    staff = Staff.objects.all()
    context = {"staff": staff}
    return render(request, "core/staff.html", context)
