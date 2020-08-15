from django.db import models
from password_manager.settings import AUTH_USER_MODEL
from cryptography.fernet import Fernet


class PasswordCategory(models.Model):
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    category_name = models.CharField("Category Name", max_length=200)

    def __str__(self):
        return str(self.created_by.username) + '-' + str(self.category_name)

    class Meta:
        verbose_name_plural = "Password Categories"


class PasswordHint(models.Model):
    linked_category = models.ForeignKey(PasswordCategory, on_delete=models.CASCADE)
    password_belongs_to = models.CharField("Password Relation", max_length=200)
    real_password = models.CharField("Actual Password", max_length=100)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    password_hint_one = models.TextField("First Hint")
    password_hint_two = models.TextField("Second Hint", null=True, blank=True)
    hint_image = models.ImageField(upload_to='hint_image')

    def __str__(self):
        return str(self.password_belongs_to) + '-' + str(self.created_by.username)

    def get_real_password(self):
        key = self.created_by.user_secret_key
        cipher_suite = Fernet(key.encode())
        real_password = cipher_suite.decrypt(self.real_password.encode())
        return real_password.decode('utf-8')

    class Meta:
        verbose_name_plural = "Password Hints"


class FileEncrypt(models.Model):
    uploaded_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_description = models.CharField("Description of the file", max_length=200)
    actual_file = models.FileField(upload_to='file_uploads')

    def __str__(self):
        return str(self.uploaded_by.username) + '-' + str(self.file_description)

    class Meta:
        verbose_name_plural = "Encrypted Files"



