from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import View

from .forms import LoginForm, SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        print(form.data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    return render(request, "accounts/signup.html")


class SignUpView(View):
    template_name = "accounts/signup.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name)


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(
                "home"
            )  # Replace 'home' with the URL name of your home page
    else:
        form = LoginForm()
    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")
