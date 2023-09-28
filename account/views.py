from typing import Any
from django import http
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post

# Create your views here.


# RegisterView
class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = "account/register.html"

    def dispatch(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password1"])
            messages.success(request, "Your registration was successful", "success")
            return redirect("home:home")
        return render(request, self.template_name, {"form": form})


# LoginView
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password1"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "log in successfully")
                return redirect("home:home")
        messages.error(request, "username or password incorrect")
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "log out successfully")
        return redirect("home:home")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, "account/profile.html", {"user": user, "posts": posts})
