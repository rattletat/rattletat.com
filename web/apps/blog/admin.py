from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Post, PostComponent, Tag


class PostComponentInline(
    SortableInlineAdminMixin, admin.StackedInline
):  # or admin.StackedInline
    model = PostComponent
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (PostComponentInline,)


admin.site.register(PostComponent)
admin.site.register(Tag)
