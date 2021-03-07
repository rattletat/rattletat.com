from autoslug import AutoSlugField
from django.db import models
from django.shortcuts import reverse
from model_utils.models import TimeStampedModel
from next_prev import next_in_order, prev_in_order


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def get_absolute_url(self):
        return reverse("blog:tag", args=[self.name])

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    title = models.CharField(max_length=250)
    slug = AutoSlugField(max_length=500, populate_from="title")
    tags = models.ManyToManyField(Tag)

    description = models.TextField()
    javascript = models.TextField(null=True, blank=True)

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


class PostComponent(models.Model):
    position = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    post = models.ForeignKey(Post, related_name="components", on_delete=models.CASCADE)

    identifier = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["position"]
