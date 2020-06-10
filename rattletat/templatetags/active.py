from django.template import Library
from django.urls import reverse

register = Library()


@register.simple_tag
def active(request, url):
    rev_url = reverse(url)
    if rev_url != "/" and rev_url in request.path:
        return "active"
    elif rev_url == request.path:
        return "active"
    return ""
