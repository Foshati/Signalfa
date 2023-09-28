from django import forms
from .models import Post


class PostCreateUpdateView(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "Image",
            "body",
        )
