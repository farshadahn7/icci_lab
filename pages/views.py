from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse

from pages.models import HomeSliderImage
from posts.models import Post


class Home(generic.ListView):
    model = HomeSliderImage
    template_name = 'index.html'
    context_object_name = 'slider_contents'

    def get_context_data(self, *, object_list=None, **kwargs):
        context_object_name = super().get_context_data(**kwargs)
        context_object_name['posts'] = Post.objects.filter(status=True)
        return context_object_name
