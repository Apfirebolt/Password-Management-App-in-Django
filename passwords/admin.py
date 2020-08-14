from django.contrib import admin
from . models import PasswordCategory, PasswordHint


admin.site.register(PasswordCategory)
admin.site.register(PasswordHint)

