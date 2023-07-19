from django.template import Library

import json

register = Library()


@register.filter(is_safe=True)
def post_to_js(posts):
    posts = list(
        map(
            lambda post: {
                "title": post.title.replace("'", ""),
                "url": post.get_absolute_url(),
                "tags": [
                    {"title": tag.name, "url": tag.get_absolute_url()}
                    for tag in post.tags.all()
                ],
            },
            posts,
        )
    )
    return json.dumps(posts)
