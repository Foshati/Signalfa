from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Image = models.ImageField(upload_to="Image/%Y/%m/%d/", blank=True, null=True)
    body = models.TextField(verbose_name="text")
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    profileImg = models.ImageField(
        upload_to="profile_images/%Y/%m/%d/", default="default.png"
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f" {self.slug} - {self.updated}"

    def get_absolute_url(self):
        return reverse("home:post_detail", args=[self.id, self.slug])

    def like_count(self):
        return self.pVote.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomment")

    reply = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="rcomment",
    )
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500, verbose_name="")
    created = models.DateTimeField(auto_now_add=True)
    create = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post.slug} - {self.user.username} - {self.body[:30]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uVote")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pVote")

    def __str__(self) -> str:
        return f"{self.user} liked {self.post.slug}"
