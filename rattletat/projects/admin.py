from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin

from .models import Project, Component


class ComponentInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Component
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ComponentInline]


admin.site.register(Project, ProjectAdmin)
