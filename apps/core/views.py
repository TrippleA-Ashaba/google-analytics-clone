from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Create your views here.


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "landing_page.html")


@login_required
def home(request):
    return render(request, "core/index.html")
