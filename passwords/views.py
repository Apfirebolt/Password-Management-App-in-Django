from django.shortcuts import render
from . forms import PasswordCategoryForm, PasswordHintForm
from . models import PasswordCategory, PasswordHint
from django.contrib import messages
from django.http import HttpResponseRedirect
from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404


@login_required
def password_home(request):
    allUserCategories = PasswordCategory.objects.filter(created_by_id=request.user.id)
    allUserPasswords = PasswordHint.objects.filter(created_by_id=request.user.id)
    return render(request, 'passwords/passwords_home.html', {
        'user_categories': allUserCategories,
        'user_passwords': allUserPasswords
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
        form = PasswordHintForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            formData = form.cleaned_data
            # Encryption using secret key and cryptography module
            secret_key = (request.user.user_secret_key).encode()
            key = Fernet.generate_key()
            cipher_suite = Fernet(secret_key)
            encrypted_string = formData['real_password']
            encoded_text = cipher_suite.encrypt(str.encode(encrypted_string))

            newPasswordObj = PasswordHint(
                created_by=request.user,
                password_belongs_to=formData['password_belongs_to'],
                linked_category=formData['linked_category'],
                real_password=encoded_text.decode('utf-8'),
                password_hint_one=formData['password_hint_one'],
                password_hint_two=formData['password_hint_two'],
                hint_image=formData['hint_image']
            )
            newPasswordObj.save()
            messages.add_message(request, messages.SUCCESS,
                                 'You have successfully created new password hint!')
            return HttpResponseRedirect(reverse('passwords:home'))
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


@login_required
def detail_password(request, pk):
    passwordDetailObj = get_object_or_404(PasswordHint, id=pk)
    return render(request, 'passwords/detail_password.html', {
        'passwordObj': passwordDetailObj
    })
