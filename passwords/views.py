from django.shortcuts import render
from . forms import PasswordCategoryForm, PasswordHintForm
from . models import PasswordCategory
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def password_home(request):
    allUserCategories = PasswordCategory.objects.filter(created_by_id=request.user.id)
    return render(request, 'passwords/passwords_home.html', {
        'user_categories': allUserCategories
    })


def create_category(request):
    if request.method == 'POST':
        form = PasswordCategoryForm(request.user, request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            categoryObj = PasswordCategory(category_name=formData['category_name'], created_by=request.user)
            categoryObj.save()
            messages.add_message(request, messages.SUCCESS,
                                 'You have successfully created new category!')
            return HttpResponseRedirect('/')
        else:
            pass
            # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordCategoryForm(request.user)
    return render(request, 'passwords/create_category.html', {'form': form})


@login_required
def create_password(request):
    if request.method == 'POST':
        form = PasswordHintForm(request.user, request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            categoryObj = PasswordCategory(category_name=formData['category_name'], created_by=request.user)
            categoryObj.save()
            messages.add_message(request, messages.SUCCESS,
                                 'You have successfully created new password hint!')
            return HttpResponseRedirect('/')
        else:
            pass
            # if a GET (or any other method) we'll create a blank form
    else:
        does_category_exist = PasswordCategory.objects.filter(created_by=request.user)
        if not does_category_exist:
            messages.add_message(request, messages.INFO,
                                 'You have not created any category! Please create one to add passwords.')
            return HttpResponseRedirect(reverse('passwords:create_category'))

        form = PasswordHintForm(request.user)
    return render(request, 'passwords/create_password.html', {'form': form})
