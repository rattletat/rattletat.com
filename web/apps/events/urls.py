from django.urls import path
from . import views

app_name = "events"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("event/<slug:event_slug>/", views.EventView.as_view(), name="event"),
]
