from django import forms
from . models import PasswordCategory, PasswordHint, FileEncrypt, GeneratedPassword
from django.core.validators import FileExtensionValidator


class PasswordCategoryForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordCategoryForm, self).__init__(*args, **kwargs)
        self.user = user

    error_messages = {
        'category_name_required': "Category Name is a required fields, cannot be left blank",
        'duplicate_category': "This Category has already been created by you."
    }
    category_name = forms.CharField(label=("Please Enter Category Name"),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PasswordCategory
        fields = ('category_name',)

    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')

        if not len(category_name):
            raise forms.ValidationError(
                self.error_messages['category_name_required'],
                code='category_name_required'
            )

        category_exists = PasswordCategory.objects.filter(created_by=self.user, category_name=category_name)
        if category_exists:
            raise forms.ValidationError(
                self.error_messages['duplicate_category'],
                code='duplicate_category'
            )

        return category_name


class PasswordHintForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(PasswordHintForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['linked_category'].queryset = PasswordCategory.objects.filter(created_by=user)

    error_messages = {
        'file_size_exceeded': "Please upload an image less than 1 MB in size.",
    }

    linked_category = forms.ModelChoiceField(queryset=None,label="Please Select Category",
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    password_belongs_to = forms.CharField(label=("Please Enter Account To Which This Password Belongs To"),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    real_password = forms.CharField(label=("Please Enter Your Password"),
                             widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_hint_one = forms.CharField(label=("Please Enter Your First Hint"),
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
    password_hint_two = forms.CharField(label=("Please Enter Your Second Hint"),
                                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    hint_image = forms.FileField(label=("Please Upload Your Profile Image"),
                                    widget=forms.FileInput(attrs={'class': 'form-control-file'}),
                                    validators=[FileExtensionValidator(['png', 'jpg'])])

    def clean_hint_image(self):
        hint_image = self.cleaned_data.get('hint_image')
        if hint_image.size > 1048576:
            raise forms.ValidationError(
                self.error_messages['file_size_exceeded'],
                code='file_size_exceeded'
            )
        return hint_image

    class Meta:
        model = PasswordHint
        fields = ('linked_category', 'password_belongs_to', 'real_password', 'password_hint_one',
                  'password_hint_two', 'hint_image',)


class GeneratedPasswordForm(forms.ModelForm):
    PASSWORD_SECURITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    password_belongs_to = forms.CharField(label=("Please Enter Account To Which This Password Belongs To"),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    security_level = forms.ChoiceField(choices=PASSWORD_SECURITY_CHOICES, label=("Please Select the Security Level For Generated Password"),
                                widget=forms.Select(attrs={'class': 'form-control'}))
    password_description = forms.CharField(required=False, label=("Please Enter Your Password Description"),
                                        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = GeneratedPassword
        fields = ('password_belongs_to', 'password_description', 'security_level',)


class UploadFileForm(forms.ModelForm):
    error_messages = {
        'file_size': "Size of the uploaded file should not exceed 5 MB",
    }
    file_description = forms.CharField(label=("File Description"),
                                    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    actual_file = forms.FileField(label=("Please Upload Your Profile Image"),
                                 widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    def clean_actual_file(self):
        actual_file = self.cleaned_data.get('actual_file')
        if actual_file.size > 5242880:
            raise forms.ValidationError(
                self.error_messages['file_size'],
                code='file_size'
            )
        return actual_file

    class Meta:
        model = FileEncrypt
        fields = ('file_description', 'actual_file',)




