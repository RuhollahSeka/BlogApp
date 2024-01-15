from ninja_extra import api_controller, ControllerBase, pagination, status, http_get, http_post, http_put, http_delete

from blog.models import Post
from ..schemas import PostResponseSchema, PostInputSchema


@api_controller('/posts')
class PostController(ControllerBase):
    @http_get('/', response=pagination.PaginatedResponseSchema[PostResponseSchema])
    @pagination.paginate(pagination.LimitOffsetPagination, limit=10, offset=0)
    def list_post(self):
        return Post.objects.all()

    @http_get('/{post_id}', response=PostResponseSchema)
    def get_post(self, post_id: int):
        return self.get_object_or_exception(Post, id=post_id)

    @http_post('/', response=PostResponseSchema)
    def create_post(self, post_data: PostInputSchema):
        return Post.objects.create(
            title=post_data.title,
            content=post_data.content,
        )

    @http_put('/{post_id}', response=PostResponseSchema)
    def update_post(self, post_id: int, post_data: PostInputSchema):
        post = self.get_object_or_exception(Post, id=post_id)
        post.title = post_data.title
        post.content = post_data.content
        post.save()
        return post

    @http_delete('/{post_id}', response={204: None})
    def delete_post(self, post_id: int):
        post = self.get_object_or_exception(Post, id=post_id)
        post.delete()
        return self.create_response(None, status_code=status.HTTP_204_NO_CONTENT)
