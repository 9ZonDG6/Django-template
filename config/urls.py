from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import URLPattern, URLResolver, include, path

from config.settings.django import MEDIA_ROOT, MEDIA_URL
from config.settings.env import DEBUG

urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
]

if DEBUG:
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
    urlpatterns.extend(staticfiles_urlpatterns())
    urlpatterns.extend(static(MEDIA_URL, document_root=MEDIA_ROOT))
