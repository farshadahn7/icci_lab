from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login_view'),
    path('logout', views.LogoutView.as_view(), name='logout_view'),
    path('signup', views.SignupView.as_view(), name='signup_view'),
]
