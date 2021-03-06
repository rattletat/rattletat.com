from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .forms import CommentForm
from .models import Comment, Post, Tag

from django.shortcuts import render
from django.template import RequestContext


class IndexView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-created"]

    def get_queryset(self):
        return Post.objects.all()


class TagView(ListView):
    template_name = "blog/tag.html"
    model = Post
    ordering = ["-created"]

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs["tag"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = Tag.objects.get(name=self.kwargs["tag"])
        return context


class PostView(DetailView):
    model = Post
    template_name = "blog/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentCreateView(CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        self.object = form.save(commit=False)
        self.object.post = post
        self.object.save()
        return redirect(post)
