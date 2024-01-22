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
        allowed_routes=['create', 'find_one', 'list', 'update', 'delete'],
        model=Post,
        create_schema=PostInputSchema,
        retrieve_schema=PostResponseSchema,
        pagination=ModelPagination(
            klass=pagination.LimitOffsetPagination,
            pagination_schema=NinjaPaginationResponseSchema,
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
