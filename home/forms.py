from django import forms

from .models import Comment, Post


class PostSearchForm(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'search...', "class": "rounded-2xl  w-[25rem]  p-2",}),
        label='',  # Make the label empty
        required=False  # Make the field not required to allow it to be empty
    )
class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "Image",
            "body",
        ]


class CommentCreateForme(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 5,
                    "cols": 40,
                    "class": "rounded-lg",
                    "placeholder": "Comment",
                }
            )
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 4,
                    "cols": 40,
                    "class": "rounded-lg text-black",
                    "placeholder": "Comment",
                    # "style": "color: black;",
                }
            )
        }


#  password2 = forms.CharField(
#         widget=forms.PasswordInput(
#             attrs={"class": "rounded-lg", "placeholder": "Confirm Password"}
#         )
#     )
