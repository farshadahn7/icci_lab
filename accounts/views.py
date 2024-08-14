from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse
from django.views import View, generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, SignupForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('pages:home')
        form = LoginForm()
        return render(request, template_name='accounts/login.html', context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.professor_verification:
                    login(request, user)
                    return JsonResponse(
                        {'status': 1, 'msg': 'Logged in successfully', 'url': reverse('panel:panel_home')})
                else:
                    return JsonResponse(
                        {'status': 2, 'msg': 'still under acceptance process from ICCI lab head.'})
            else:
                return JsonResponse(
                    {'status': 3, 'msg': 'Username or password is incorrect'})
        else:
            return JsonResponse(
                {'status': 3, 'msg': 'Username or password is incorrect'})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('pages:home')


class SignupView(generic.CreateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        form = SignupForm()
        return render(request, template_name='accounts/signup.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {'status': 1, 'msg': 'registered successfully. Message sent for ICCI LAB head for verification.'})
        else:
            return JsonResponse(
                {'status': 3, 'msg': form.errors})


class CurrentView(generic.TemplateView):
    template_name = 'members/current.html'


class AlumniView(generic.TemplateView):
    template_name = 'members/Alumni.html'
