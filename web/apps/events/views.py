from django.views.generic import ListView, DetailView

from .models import Event


class IndexView(ListView):
    template_name = "events/index.html"
    model = Event
    ordering = ["-created"]

    def get_queryset(self):
        return Event.objects.all()


class EventView(DetailView):
    model = Event
    template_name = "events/event.html"

    def get_object(self):
        event_slug = self.kwargs["event_slug"]
        return Event.objects.get(slug=event_slug)
