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
