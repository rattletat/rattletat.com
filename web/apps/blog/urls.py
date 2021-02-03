from django.urls import path
from . import views
from .feed import LatestPostsFeed, LatestTagPostFeed

app_name = "blog"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.PostView.as_view(), name="post"),
    path("<int:pk>/comment", views.CommentCreateView.as_view(), name="comment"),
    path("tag/<tag>/", views.TagView.as_view(), name="tag"),
    path("feed/", LatestPostsFeed(), name="feed"),
    path("feed/<tag>/", LatestTagPostFeed()),
]
