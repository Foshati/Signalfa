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

    def __str__(self):
        return f" {self.slug} - {self.updated}"

    def get_absolute_url(self):
        return reverse("home:post_detail", args=[self.id, self.slug])
