from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
# Create your views here.

from .forms import CustomUserCreationForm, CustomUserChangeForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UpdateUserView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('login')
    template_name = 'registration/edit_account.html'



#class LoginView(CreateView):        #PROTOTYPE NOT USED
    #form_class = CustomLoginForm
    #success_url = reverse_lazy('home')
    #template_name = 'registration/login.html'

