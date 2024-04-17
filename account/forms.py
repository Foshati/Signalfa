from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "User",
                "class": "rounded-lg",
            }
        ),
        max_length=10,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "email@gmail.com", "class": "rounded-lg"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "rounded-lg", "placeholder": "Enter Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "rounded-lg", "placeholder": "Confirm Password"}
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("This Email is already in use")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError("This username is already in use")
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords must match")


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "user name", "class": "rounded-lg"}
        ),
        max_length=20,
        label="User Name",
    )
    password1 = forms.CharField(
        label="password",
        widget=forms.PasswordInput(
            attrs={"class": "rounded-lg", "placeholder": " Password"}
        ),
    )


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ["age", "bio"]
