from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin

from .models import Project, Component


class ComponentInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Component
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ComponentInline]


admin.site.register(Project, ProjectAdmin)
