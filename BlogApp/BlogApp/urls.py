from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from blog.api import urls as blog_urls

auth_api = NinjaExtraAPI(app_name='auth', urls_namespace='auth')
auth_api.register_controllers(NinjaJWTDefaultController)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', blog_urls),
    path('api/', auth_api.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
