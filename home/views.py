from typing import Any
from django import http

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import slugify
from django.views import View

from .forms import (
    PostCreateUpdateForm,
    CommentCreateForme,
    CommentReplyForm,
    PostSearchForm,
)
from .models import Post, Comment, Vote

# Create your views here.


def home(request):
    return render(request, "home/index.html")


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get("search"):
            posts = posts.filter(body__contains=request.GET["search"])
        return render(
            request, "home/index.html", {"posts": posts, "form": self.form_class}
        )


# Detail view
class PostDetailView(View):
    form_class = CommentCreateForme
    form_class_reply = CommentReplyForm

    def setup(self, request, *args: Any, **kwargs: Any) -> None:
        self.post_instance = get_object_or_404(
            Post, pk=kwargs["post_id"], slug=kwargs["post_slug"]
        )
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomment.filter(is_reply=False)
        return render(
            request,
            "home/detail.html",
            {
                "post": self.post_instance,
                "comments": comments,
                "form": self.form_class,
                "reply_form": self.form_class_reply,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, "your comment was added")
            return redirect(
                "home:post_detail", self.post_instance.id, self.post_instance.slug
            )
        else:
            messages.error(request, "your comment was not added")
            return redirect(
                "home:post_detail", self.post_instance.id, self.post_instance.slug
            )


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
    form_class = PostCreateUpdateForm

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
    form_class = PostCreateUpdateForm

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


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "Your comment has been sent")
        return redirect("home:post_detail", post.id, post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, "you have already liked this post")
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, "you liked this post")
        return redirect("home:post_detail", post.id, post.slug)
