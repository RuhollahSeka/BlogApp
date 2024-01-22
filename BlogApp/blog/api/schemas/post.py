from django.contrib.auth.models import User
from ninja import ModelSchema

from blog.models import Post


class PostUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class PostResponseSchema(ModelSchema):
    user: PostUserSchema

    class Meta:
        model = Post
        fields = (
            'id',
            'created_at',
            'updated_at',
            'title',
            'content',
        )


class PostInputSchema(ModelSchema):
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
        )
