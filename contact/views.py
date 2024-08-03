from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse

from contact.forms import ContactForm
from contact.models import Contact


class ContactView(generic.CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'

    def form_valid(self, form):
        form.save()
        return JsonResponse({'status': 1, 'msg': 'Message sent successfully.'})

    def form_invalid(self, form):
        return JsonResponse({'status': 2, 'msg': 'opps somthing went wrong tyr again later'})

# Create your views here.
