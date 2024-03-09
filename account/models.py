from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Relation(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Rfrom_user"
    )
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Rto_user")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.from_user} following {self.to_user}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
