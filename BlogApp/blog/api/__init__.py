from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from . import controllers

api = NinjaExtraAPI(app_name='blogs')
api.register_controllers(
    NinjaJWTDefaultController,
    controllers.PostModelController,
)
urls = api.urls
