from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.


# RegisterView
class RegisterView(View):
    form_class = UserRegisterForm
    template_name = "account/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password"])
            messages.success(request, "Your registration was successful", "success")
            return redirect("home:home")
        return render(request, self.template_name, {"form": form})
