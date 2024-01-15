from ninja import ModelSchema, Schema

from blog.models import Post


class PostResponseSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = (
            'id',
            'created_at',
            'updated_at',
            'title',
            'content',
        )


class PostInputSchema(ModelSchema):
    class Config:
        model = Post
        model_fields = (
            'title',
            'content',
        )
