from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from django.shortcuts import render

from posts.forms import PostForm
from posts.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context_object_name = super().get_context_data(**kwargs)
        context_object_name['latest_posts'] = Post.objects.order_by('-created_at')[0:2]
        return context_object_name
