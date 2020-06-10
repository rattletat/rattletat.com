from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.text import slugify
import os


class Project(TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)

    def _image_path(self, filename):
        return os.path.join(self.root_path, "images", filename)

    image = models.ImageField(upload_to=_image_path)

    @property
    def root_path(self):
        return os.path.join("projects", slugify(self.title))

    def __str__(self):
        return self.title
