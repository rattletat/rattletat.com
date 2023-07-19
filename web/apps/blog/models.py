import os
from autoslug import AutoSlugField
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
from next_prev import next_in_order, prev_in_order
from polymorphic.models import PolymorphicModel


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def get_absolute_url(self):
        return reverse("blog:tag", args=[self.name])

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    title = models.CharField(max_length=250)
    slug = AutoSlugField(max_length=500, populate_from="title")
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    description = models.TextField()
    fediverse_post = models.CharField(max_length=250, null=True, blank=True)

    def _image_path(self, filename):
        return os.path.join(self.root_path, "images", filename)

    image = models.ImageField(null=True, blank=True, upload_to=_image_path)

    @property
    def root_path(self):
        return os.path.join("posts", slugify(self.title))

    def next(self):
        return next_in_order(self)

    def previous(self):
        return prev_in_order(self)

    def get_absolute_url(self):
        return reverse("blog:post", args=[self.slug])

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.CharField(max_length=60)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.author} on Post '{self.post}': {self.text}"


class PostComponent(PolymorphicModel):
    position = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    # identifier = models.CharField(max_length=100, null=True, blank=True)

    # def __str__(self):
    #     return self.content

    class Meta:
        ordering = ["position"]


class TextComponent(PostComponent):
    content = models.TextField()


class ImageComponent(PostComponent):
    def _image_path(self, filename):
        return os.path.join(self.post.root_path, "images", filename)

    image = models.ImageField(upload_to=_image_path)
    description = models.TextField(null=True, blank=True)


class PlotComponent(PostComponent):
    # identifier = models.CharField(max_length=100, null=True, blank=True)
    javascript = models.TextField(null=True, blank=True)
