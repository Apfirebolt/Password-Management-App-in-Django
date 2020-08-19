from django.shortcuts import render
from . forms import PasswordCategoryForm, PasswordHintForm
from . models import PasswordCategory, PasswordHint
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from cryptography.fernet import Fernet
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


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
    if passwordDetailObj.created_by_id != request.user.id:
        raise PermissionDenied()
    return render(request, 'passwords/detail_password.html', {
        'passwordObj': passwordDetailObj
    })


@login_required
def delete_password(request, pk):
    if request.method == 'POST':
        try:
            password_hint_obj = PasswordHint.objects.get(id=pk)
            if password_hint_obj.created_by_id != request.user.id:
                raise PermissionDenied()
            password_hint_obj.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Password hint was successfully updated!')
            return HttpResponseRedirect(reverse('passwords:home'))
        except Exception as err:
            print(err)
            return HttpResponse('Some error occurred')
    else:
        passwordHintObj = PasswordHint.objects.get(id=pk)
        return render(request, 'passwords/delete_password.html', {
            'password_obj': passwordHintObj
        })


@login_required
def update_hints(request, pk):
    if request.method == 'POST':
        try:
            password_hint_obj = PasswordHint.objects.get(id=pk)
            first_hint = request.POST.get('first_password_hint')
            second_hint = request.POST.get('second_password_hint')

            password_hint_obj.password_hint_one = first_hint
            password_hint_obj.password_hint_two = second_hint
            if request.FILES.get('hint_image_changed'):
                password_hint_obj.hint_image = request.FILES.get('hint_image_changed')
            password_hint_obj.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Passwords hints successfully updated!')
            return HttpResponseRedirect(reverse('passwords:home'))
        except Exception as err:
            print(err)
            return HttpResponse('Some error occurred')
    else:
        passwordHintObj = PasswordHint.objects.get(id=pk)
        if passwordHintObj.created_by_id != request.user.id:
            raise PermissionDenied()
        return render(request, 'passwords/update_hints.html', {
            'password_obj': passwordHintObj
        })


@login_required
def update_password(request, pk):
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

            passwordHintObj = PasswordHint.objects.get(id=pk)
            # Updating values
            passwordHintObj.password_belongs_to = formData['password_belongs_to']
            passwordHintObj.password_hint_one = formData['password_hint_one']
            passwordHintObj.password_hint_two = formData['password_hint_two']
            passwordHintObj.linked_category = formData['linked_category']
            passwordHintObj.real_password = encoded_text.decode('utf-8')
            passwordHintObj.hint_image = formData['hint_image']

            passwordHintObj.save()
            messages.add_message(request, messages.SUCCESS,
                                 'You have successfully updated your password hint!')
            return HttpResponseRedirect(reverse('passwords:home'))
        else:
            pass
    else:
        passwordHintObj = PasswordHint.objects.get(id=pk)
        if passwordHintObj.created_by_id != request.user.id:
            raise PermissionDenied()
        initialData = {
            'password_belongs_to': passwordHintObj.password_belongs_to,
            'linked_category': passwordHintObj.linked_category,
            'password_hint_one': passwordHintObj.password_hint_one,
            'password_hint_two': passwordHintObj.password_hint_two,
            'hint_image': passwordHintObj.hint_image
        }
        form = PasswordHintForm(request.user, initial=initialData)
    return render(request, 'passwords/update_password.html', {'form': form})
