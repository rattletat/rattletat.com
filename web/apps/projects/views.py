from .models import Project
from django.views.generic import ListView, DetailView


class IndexView(ListView):
    template_name = "projects/index.html"
    model = Project
    ordering = ["-created"]

    def get_queryset(self):
        return Project.objects.all()


class ProjectView(DetailView):
    model = Project
    template_name = "projects/detail.html"

    def get_object(self):
        project_slug = self.kwargs["project_slug"]
        return Project.objects.get(slug=project_slug)
