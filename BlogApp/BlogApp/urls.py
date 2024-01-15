from django.contrib import admin
from django.urls import path

from blog.api import urls as blog_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', blog_urls),
]
