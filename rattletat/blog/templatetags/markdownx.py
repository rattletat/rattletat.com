from django import template
from rattletat.blog.utils.secure_markdown import markdownify

register = template.Library()


@register.filter
def show_markdown(text):
    return markdownify(text)
