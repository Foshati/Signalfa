from django import forms


class UserRegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "sam", "class": "rounded-lg"}),
        max_length=10,
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "email@gmail.com", "class": "rounded-lg"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "rounded-lg", "placeholder": "2598dsf247@$#%"}
        )
    )
