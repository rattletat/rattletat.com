from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from markdownx import urls as markdownx_urls

from rattletat.blog import urls as blog_urls
from rattletat.projects import urls as projects_urls
from rattletat.startpage import views as startpage_views

urlpatterns = [
    path("", startpage_views.view_startpage, name="startpage"),
    path("projects/", include(projects_urls, namespace="projects")),
    path("blog/", include(blog_urls, namespace="blog")),
    path("admin/", admin.site.urls),
    path("markdownx/", include(markdownx_urls)),
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
