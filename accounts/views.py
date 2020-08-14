from django.shortcuts import render
from django.views.generic import View, TemplateView
from . forms import CustomUserForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import reverse


class AccountsHome(TemplateView):
    template_name = 'accounts/dashboard.html'


def create_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO,
                                 'You have successfully registered! Please continue to your dashboard!')
            return HttpResponseRedirect('/')
        else:
            pass
            # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomUserForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        userEmail = request.POST['email']
        userPassword = request.POST['password']

        user = authenticate(username=userEmail, password=userPassword)
        if user is not None:
            messages.add_message(request, messages.INFO,
                                 'You have successfully logged in! Please continue to your dashboard!')
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Invalid credentials provided, failed to login!')
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        return render(request, 'accounts/login.html', {})
