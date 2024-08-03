from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse

from pages.models import HomeSliderImage


class Home(generic.ListView):
    model = HomeSliderImage
    template_name = 'index.html'
    context_object_name = 'slider_contents'
