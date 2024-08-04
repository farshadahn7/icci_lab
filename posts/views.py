from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from django.shortcuts import render

from posts.forms import PostForm
from posts.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'

