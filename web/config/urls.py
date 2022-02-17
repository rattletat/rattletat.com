from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages import views as flat_views
from django.urls import include, path

from apps.blog import urls as blog_urls
from apps.projects import urls as projects_urls
from apps.startpage import views as startpage_views

urlpatterns = [
    path("", startpage_views.view_startpage, name="startpage"),
    path("projects/", include(projects_urls, namespace="projects")),
    path("blog/", include(blog_urls, namespace="blog")),
    path("about/", flat_views.flatpage, {"url": "/about/"}, name="about"),
    path("privacy/", flat_views.flatpage, {"url": "/privacy/"}, name="privacy"),
    path(settings.ADMIN_URL, admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = urlpatterns + [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    from django.conf.urls.static import static

    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
