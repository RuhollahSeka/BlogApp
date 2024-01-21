from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    title = models.CharField(
        max_length=200,
    )

    content = models.TextField()

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
