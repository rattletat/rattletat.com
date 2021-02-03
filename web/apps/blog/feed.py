from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = "Rattletat Blog"
    link = "/feed/"
    description = "Latest Posts"

    def items(self):
        return Post.objects.order_by("-created")[:5]

    def item_description(self, post):
        return truncatewords(post.text, 50)


class LatestTagPostFeed(Feed):
    title = "Rattletat Blog"
    description = "Latest Posts"
    link = ""

    def get_object(self, request, tag):
        return tag

    def items(self, tag):
        print(tag)
        return Post.objects.filter(tags__name=tag).order_by("-created")[:5]

    def item_description(self, post):
        return truncatewords(post.text, 50)
