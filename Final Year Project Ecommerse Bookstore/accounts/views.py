
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views import generic


class SignUpView(generic.CreateView):
    _class    = UserCreationForm
    success_url   = reverse_lazy('login')
    template_name = 'signup.html'