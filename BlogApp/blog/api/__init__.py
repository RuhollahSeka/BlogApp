from ninja_extra import NinjaExtraAPI

from .controllers import PostController

api = NinjaExtraAPI(app_name='blogs')
api.register_controllers(
    PostController,
)
urls = api.urls
