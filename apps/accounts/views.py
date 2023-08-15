from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import LoginForm, SignUpForm
from django.views.generic import CreateView


# def signup(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         print(form.data)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("home")

#     return render(request, "accounts/signup.html")


# class SignUpView(View):
#     template_name = "accounts/signup.html"

#     def get(self, request):
#         form = SignUpForm()
#         return render(request, self.template_name, {"form": form})

#     def post(self, request):
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("home")
#         return render(request, self.template_name)


class SignUpView(CreateView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Call the parent class's form_valid method to save the user
        response = super().form_valid(form)

        # Authenticate and log in the user
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)

        return response


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
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")
