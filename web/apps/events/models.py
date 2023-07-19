import os
from autoslug import AutoSlugField
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from next_prev import next_in_order, prev_in_order

from apps.blog.models import Tag


class Event(TimeStampedModel):
    title = models.CharField(max_length=250)
    slug = AutoSlugField(max_length=500, populate_from="title")
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    # fediverse_post = models.CharField(max_length=250, null=True, blank=True)

    def _image_path(self, filename):
        return os.path.join(self.root_path, "images", filename)

    image = models.ImageField(null=True, blank=True, upload_to=_image_path)

    @property
    def root_path(self):
        return os.path.join("events", slugify(self.title))

    def next(self):
        return next_in_order(self)

    def previous(self):
        return prev_in_order(self)

    def get_absolute_url(self):
        return reverse("events:event", args=[self.slug])

    def __str__(self):
        return self.title
