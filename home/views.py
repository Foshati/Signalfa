from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify
from django.views import View

from .forms import PostCreateUpdateView
from .models import Post

# Create your views here.


def home(request):
    return render(request, "home/index.html")


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "home/index.html", {"posts": posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        return render(request, "home/detail.html", {"post": post})


# delete Form
class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "The post was deleted")
        else:
            messages.error(request, "you can t delete this post")
        return redirect("home:home")


# update Form
class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateView

    def setup(self, request, *args: Any, **kwargs: Any):
        self.post_instance = get_object_or_404(Post, pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "you can not change this page")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, "home/update.html", {"form": form, "post": post})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.save()
            messages.success(request, "you updated this post")
            return redirect("home:post_detail", post.id, post.slug)


# create form view


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateView

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, "home/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid:
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["body"][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, "created post successfully")
            return redirect("home:post_detail", new_post.id, new_post.slug)
