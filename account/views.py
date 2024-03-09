from typing import Any
from django import http

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View

from home.models import Post

from .forms import UserLoginForm, UserRegisterForm, EditUserForm
from .models import Relation

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

    def setup(self, request, *args: Any, **kwargs: Any) -> None:
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

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
                if self.next:
                    return redirect(self.next)

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
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(
            request,
            "account/profile.html",
            {"user": user, "posts": posts, "is_following": is_following},
        )


class UserPasswordRestView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, "You followed this user")
        else:
            Relation(from_user=request.user, to_user=user).save()
            # Relation.objects.create(from_user=request.user, to_user=user)
            messages.success(request, "You have followed this user")
        return redirect("account:user_profile", user.id)


# unfollow View
class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, "You have unfollowed this user")
        else:
            messages.success(request, "You are not following this user")
        return redirect("account:user_profile", user.id)


# Edit profile View
class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self, request):
        form = self.form_class(
            instance=request.user.profile, initial={"email": request.user.email}
        )

        return render(request, "account/edit_profile.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            messages.success(request, "Your profile has been successfully changed")
        return redirect("account:user_profile", request.user.id)
