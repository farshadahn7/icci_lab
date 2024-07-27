from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View, generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, SignupForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
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
                    return redirect('home')
                else:
                    return JsonResponse({'msg': 'still under acceptance process from ICCI lab head.'})
            else:
                return JsonResponse({'msg': 'username or password is incorrect.'})
        else:
            return JsonResponse({'msg': form.errors})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


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
            return JsonResponse({'msg': 'registered successfully. Message sent for ICCI LAB head for verification.'})
        else:
            return JsonResponse({'msg': form.errors})
