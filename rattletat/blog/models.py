from django.db import models
from django.shortcuts import reverse
from model_utils.models import TimeStampedModel
from next_prev import next_in_order, prev_in_order


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse("blog:tag", args=[self.name])

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    tags = models.ManyToManyField(Tag, related_name="posts")

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    text = models.TextField()

    def next(self):
        return next_in_order(self)

    def previous(self):
        return prev_in_order(self)

    def get_absolute_url(self):
        return reverse("blog:post", args=[self.pk])

    def __str__(self):
        return self.title


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=60)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.author} on Post '{self.post}': {self.text}"
