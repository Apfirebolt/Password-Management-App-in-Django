from django import forms
from . models import CustomUser
from cryptography.fernet import Fernet
from django.core.validators import FileExtensionValidator
from django.contrib.auth import authenticate
import re


class CustomUserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
        'username_required': ("User name is a required field."),
        'username_rules': "User name must not contain any special character aside from space.",
        'valid_images': "Image uploaded is not in valid form, must be in png or jpg format!",
        'password_length': "Your password is not secure enough, must be at least 8 characters long.",
        'password_security': "Your password must contain at least 1 number and a capital letter."
    }
    password1 = forms.CharField(label=("Please Enter Your Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=("Please Confirm Your Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=("Enter the same password as above, for verification."))
    username = forms.CharField(label=("Please Enter Username"),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=("Please Enter Your Email"),
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_image = forms.FileField(label=("Please Upload Your Profile Image"),
                                    widget=forms.FileInput(attrs={'class': 'form-control-file'}),
                                    validators=[FileExtensionValidator(['png', 'jpg'])])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_image',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(
                self.error_messages['username_required'],
                code='username_required'
            )

        pattern = '^[^0-9][a-zA-Z0-9_ ]+$'
        result = re.match(pattern, username)

        if username and not result:
            raise forms.ValidationError(
                self.error_messages['username_rules'],
                code='username_rules'
            )
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise forms.ValidationError(
                self.error_messages['password_length'],
                code='password_length'
            )
        pattern = '[A-Za-z0-9@#$%^&+=]+'
        result = re.fullmatch(pattern, password)

        if len(password) > 8 and not result:
            raise forms.ValidationError(
                self.error_messages['password_security'],
                code='password_security'
            )

        return password

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_secret_key = Fernet.generate_key().decode('utf-8') #this is your cryptography "secret key"

        if commit:
            user.save()
        return user


class UpdateSettingsForm(forms.ModelForm):
    error_messages = {
        'username_required': ("User name is a required field."),
        'username_rules': "User name must not contain any special character aside from space.",
    }
    username = forms.CharField(required=True, label=("Please Enter Your Username"),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label=("Please Enter Your Email"),
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError(
                self.error_messages['username_required'],
                code='username_required'
            )

        pattern = '^[^0-9][a-zA-Z0-9_ ]+$'
        result = re.match(pattern, username)

        if username and not result:
            raise forms.ValidationError(
                self.error_messages['username_rules'],
                code='username_rules'
            )
        return username

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class UpdateProfileImageForm(forms.ModelForm):
    error_messages = {
        'image_size': "Image uploaded should not be larger than 1 MB, please upload another image!",
    }
    profile_image = forms.FileField(label=("Please Upload Your Profile Image"),
                                    widget=forms.FileInput(attrs={'class': 'form-control-file'}),
                                    validators=[FileExtensionValidator(['png', 'jpg'])])

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image.size > 1048576:
            raise forms.ValidationError(
                self.error_messages['image_size'],
                code='image_size'
            )
        return profile_image

    class Meta:
        model = CustomUser
        fields = ('profile_image',)


class UpdatePasswordForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    error_messages = {
        'wrong_password': "Previous Password you entered is wrong. Please enter a correct password or use forget password.",
        'password_length': "Your password is not strong enough, must be at least 8 characters long.",
        'password_strength': "Your password is not strong enough, must be at least 8 characters long and should"
                             "have at least 1 Block letter and a number!",
    }
    old_password = forms.CharField(label=("Please Enter Your Old Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label=("Please Enter Your New Password"),
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = authenticate(username=self.user.email, password=old_password)
        if user is None:
            raise forms.ValidationError(
                self.error_messages['wrong_password'],
                code='wrong_password'
            )
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        if len(new_password) < 8:
            raise forms.ValidationError(
                self.error_messages['password_length'],
                code='password_length'
            )
        pattern = '[A-Za-z0-9@#$%^&+=]+'
        result = re.fullmatch(pattern, new_password)

        if len(new_password) > 8 and not result:
            raise forms.ValidationError(
                self.error_messages['password_strength'],
                code='password_strength'
            )

        return new_password

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password',)


