from django.template import Library

import json

register = Library()


@register.filter(is_safe=True)
def event_to_js(events):
    events = list(
        map(
            lambda event: {
                "title": event.title.replace("'", ""),
                "url": event.get_absolute_url(),
                "tags": [
                    {"title": tag.name, "url": tag.get_absolute_url()}
                    for tag in event.tags.all()
                ],
            },
            events,
        )
    )
    return json.dumps(events)
