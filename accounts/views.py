from django.shortcuts import render
from django.views.generic import View, TemplateView
from . forms import CustomUserForm
from . models import CustomUser
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required


class AccountsHome(LoginRequiredMixin, TemplateView):
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
            login(request, user)
            messages.add_message(request, messages.INFO,
                                 'You have successfully logged in! Please continue to your dashboard!')
            return HttpResponseRedirect(reverse('accounts:home'))
        else:
            messages.add_message(request, messages.ERROR,
                                 'Invalid credentials provided, failed to login!')
            return HttpResponseRedirect(reverse('accounts:login'))
    else:
        return render(request, 'accounts/login.html', {})


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS,
                         'Successfully logged out, Please login to continue!')
    return HttpResponseRedirect(reverse('accounts:login'))


@login_required
def update_settings(request):
    if request.method == 'POST':
        formData = request.POST
        userObj = CustomUser.objects.get(id=request.user.id)
        userObj.email = formData['email']
        userObj.username = formData['username']
        userObj.save()
        messages.add_message(request, messages.SUCCESS,
                             'You have successfully updated your email/username settings.')
        return HttpResponseRedirect(reverse('accounts:home'))
    else:
        userObj = CustomUser.objects.get(id=request.user.id)
        return render(request, 'accounts/update_settings.html', {
            'user_data': userObj
        })


@login_required
def update_profile_image(request):
    if request.method == 'POST':
        profileImage = request.FILES['profile_image']
        userObj = CustomUser.objects.get(id=request.user.id)
        userObj.profile_image = profileImage
        userObj.save()
        messages.add_message(request, messages.SUCCESS,
                             'Your Profile Image was successfully updated!')
        return HttpResponseRedirect(reverse('accounts:home'))
    else:
        userObj = CustomUser.objects.get(id=request.user.id)
        return render(request, 'accounts/update_profile_image.html', {
            'user_data': userObj
        })


def update_password(request):
    if request.method == 'POST':
        try:
            formData = request.POST
            old_password = formData['old_password']
            new_password = formData['new_password']
            userObj = CustomUser.objects.get(id=request.user.id)

            user = authenticate(username=userObj.email, password=old_password)
            if user is not None:
                userObj.set_password(new_password)
                userObj.save()
                messages.add_message(request, messages.SUCCESS,
                                     '%s , Your Password was successfully updated!' % userObj.username)
                return HttpResponseRedirect(reverse('accounts:home'))
        except Exception as err:
            print(err)
            return HttpResponse('Some error')
    else:
        return render(request, 'accounts/update_password.html', {})