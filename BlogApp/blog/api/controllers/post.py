from typing import Any

from ninja_extra import api_controller, pagination, ModelControllerBase, ModelConfig, ModelPagination, ModelService
from ninja_extra.schemas import NinjaPaginationResponseSchema
from ninja_jwt.authentication import JWTAuth
from pydantic import BaseModel as PydanticModel

from blog.models import Post
from ..schemas import PostResponseSchema, PostInputSchema


@api_controller('/posts', auth=JWTAuth())
class PostModelController(ModelControllerBase, ModelService):
    model_config = ModelConfig(
        model=Post,
        create_schema=PostInputSchema,
        retrieve_schema=PostResponseSchema,
        patch_schema=PostInputSchema,
        pagination=ModelPagination(
            klass=pagination.LimitOffsetPagination,
            pagination_schema=NinjaPaginationResponseSchema,
            pagination_kwargs={
                'limit': 10,
                'offset': 0,
            },
        )
    )

    def __init__(self):
        ModelService.__init__(self, model=Post)
        self.service = self

    def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
        user = self.context.request.user
        if user.is_authenticated:
            kwargs['user'] = user
        return super().create(schema, **kwargs)
