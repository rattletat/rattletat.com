from django.template import Library
from django.urls import reverse

register = Library()


@register.simple_tag
def active(request_path, url):
    rev_url = reverse(url)
    if rev_url != "/" and rev_url in request_path:
        return "active"
    elif rev_url == request_path:
        return "active"
    return ""
