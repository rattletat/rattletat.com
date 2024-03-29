import os

from django.db import models
from django.shortcuts import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify
from model_utils.models import TimeStampedModel

from apps.blog.models import Post


class Project(TimeStampedModel):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(max_length=500, populate_from="title")
    description = models.TextField()

    def _image_path(self, filename):
        return os.path.join(self.root_path, "images", filename)

    image = models.ImageField(upload_to=_image_path)

    @property
    def root_path(self):
        return os.path.join("projects", slugify(self.title))

    def get_absolute_url(self):
        return reverse("projects:detail", args=[self.pk])

    def __str__(self):
        return self.title


class Component(models.Model):
    project = models.ForeignKey(Project, models.CASCADE)
    position = models.PositiveSmallIntegerField(default=0, editable=True, db_index=True)
    post = models.ForeignKey(Post, models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        if self.post:
            return reverse("blog:post", args=[self.post])
        else:
            return reverse("projects:detail", args=[self.pk])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["position"]
