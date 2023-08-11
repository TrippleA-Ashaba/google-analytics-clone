from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BusinessForm
from .models import Business

# Create your views here.


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "landing_page.html")


@login_required
def home(request):
    return render(request, "core/index.html")


def business_register(request):
    if request.method == "POST":
        form = BusinessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "core/business_register.html")


def show_businesses(request):
    businesses = Business.objects.all()
    context = {"businesses": businesses}
    return render(request, "core/businesses.html", context)
