from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Post, Tag


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, MarkdownxModelAdmin)
admin.site.register(Tag, TagAdmin)
